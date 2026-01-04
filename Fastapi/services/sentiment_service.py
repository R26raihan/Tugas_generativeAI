"""
Sentiment analysis service.
"""
from transformers import pipeline
from collections import Counter
from typing import Dict, List, Tuple
import json
import csv


class SentimentService:
    """Handles sentiment analysis using NLP models."""
    
    def __init__(self, device_index: int):
        """
        Initialize sentiment analyzer.
        
        Args:
            device_index: Device index for pipeline (-1 for CPU, 0 for GPU)
        """
        print("Memuat model sentiment analysis...")
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis", 
            model="distilbert-base-multilingual-cased", 
            device=device_index
        )
        print("Model sentiment analysis siap!")
    
    def analyze_data(self, all_headlines: Dict[str, Dict[str, List[str]]], keyword: str) -> Dict:
        """
        Analyze sentiment of headlines containing the keyword.
        
        Args:
            all_headlines: Dictionary of headlines organized by source and category
            keyword: Keyword to filter headlines
        
        Returns:
            Dictionary containing analysis results
        """
        keyword = keyword.lower()

        # Kumpulkan semua data yang relevan
        relevant_headlines: List[Tuple[str, str, str]] = [
            (source, category, headline)
            for source, categories in all_headlines.items()
            for category, headlines in categories.items()
            for headline in headlines
            if keyword in headline.lower()
        ]

        if not relevant_headlines:
            return {"message": f"Tidak ada data yang mengandung keyword '{keyword}'."}

        # Analisis sentimen dengan NLP
        sentiment_counts = {"Positif": 0, "Negatif": 0, "Netral": 0}
        examples = {"Positif": [], "Negatif": [], "Netral": []}
        source_counts = Counter([source for source, _, _ in relevant_headlines])
        category_counts = Counter([category for _, category, _ in relevant_headlines])

        print("Menganalisis sentimen dengan NLP...")
        texts = [text[:512] for _, _, text in relevant_headlines]  # Batch processing
        results = self.sentiment_analyzer(texts)

        detailed_results = []
        for (source, category, text), result in zip(relevant_headlines, results):
            label = result["label"]
            score = result["score"]

            if label == "POSITIVE" and score > 0.6:
                sentiment = "Positif"
            elif label == "NEGATIVE" and score > 0.6:
                sentiment = "Negatif"
            else:
                sentiment = "Netral"

            sentiment_counts[sentiment] += 1
            if len(examples[sentiment]) < 3:
                examples[sentiment].append({"source": source, "category": category, "text": text})

            detailed_results.append({
                "source": source,
                "category": category,
                "text": text,
                "sentiment": sentiment,
                "score": float(score)
            })

        total_relevant = len(relevant_headlines)
        sentiment_summary = {
            sentiment: {
                "count": count,
                "percentage": count / total_relevant * 100 if total_relevant > 0 else 0,
                "examples": examples[sentiment]
            }
            for sentiment, count in sentiment_counts.items()
        }

        # Struktur JSON untuk respons
        response = {
            "keyword": keyword,
            "total_items": total_relevant,
            "sentiment_summary": sentiment_summary,
            "source_distribution": dict(source_counts),
            "category_distribution": dict(category_counts),
            "detailed_results": detailed_results
        }

        # Simpan ke file CSV
        csv_filename = f"data_{keyword}_news_nlp.csv"
        with open(csv_filename, "w", encoding="utf-8", newline='') as f:
            if detailed_results:
                fieldnames = ["source", "category", "text", "sentiment", "score"]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(detailed_results)
        print(f"Data disimpan ke '{csv_filename}'")

        return response


# Global sentiment service instance (will be initialized in main.py)
sentiment_service = None
