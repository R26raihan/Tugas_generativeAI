"""
Device configuration for ML models.
Detects and configures the best available device (CUDA, MPS, or CPU).
"""
import torch


def get_device_config():
    """
    Detects the best available device for ML model execution.
    
    Returns:
        tuple: (device, device_name, device_index)
            - device: torch.device object
            - device_name: str, human-readable device name
            - device_index: int, device index for pipeline (-1 for CPU, 0 for GPU)
    """
    if torch.cuda.is_available():
        device = torch.device("cuda")
        device_name = torch.cuda.get_device_name(0)
        device_index = 0
        print(f"CUDA tersedia. Menggunakan perangkat: {device_name}")
    elif torch.backends.mps.is_available():
        device = torch.device("mps")
        device_name = "Apple Silicon (MPS)"
        device_index = 0
        print(f"MPS tersedia. Menggunakan perangkat: {device_name}")
    else:
        device = torch.device("cpu")
        device_name = "CPU"
        device_index = -1
        print("Menggunakan CPU (tidak ada GPU yang terdeteksi)")
    
    return device, device_name, device_index
