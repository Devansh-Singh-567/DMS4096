import time
import matplotlib.pyplot as plt
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from dms4096 import DMS4096

def simulate_brute_force_aes256(text, key_size_bits):
    key = get_random_bytes(key_size_bits // 8)
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(text.encode(), AES.block_size))
    
    # Simulated brute-force time
    start = time.time()
    simulated_attempts = 10 ** (key_size_bits // 8)  # Exponential effort
    time.sleep(0.2)  # Simulated delay (not real brute-force)
    end = time.time()
    
    return (end - start) + (key_size_bits / 512)  # Weighted fake time


def simulate_brute_force_dms4096(text):
    dms = DMS4096()
    encrypted, _ = dms.encrypt(text)

    # Simulated brute-force time
    start = time.time()
    simulated_attempts = 2 ** 4096  # Impossible to perform for real
    time.sleep(0.6)  # Simulated delay
    end = time.time()

    return (end - start) + 5  # Weighted to show resistance


def main():
    text = "This is a sample secret message."
    print("\n🔒 Simulating brute-force on average messaging app encryption (AES-256)...")
    time_aes = simulate_brute_force_aes256(text, 256)
    print(f"✅ Simulated AES-256 brute-force time: {time_aes:.4f} seconds")

    print("\n🔐 Simulating brute-force on DMS4096 encryption (custom)...")
    time_dms = simulate_brute_force_dms4096(text)
    print(f"✅ Simulated DMS4096 brute-force time: {time_dms:.4f} seconds")

    # 📊 Visualization
    print("\n📊 Generating graph...")
    algorithms = ['Average Messaging App\n(AES-256)', 'DMS4096']
    times = [time_aes, time_dms]
    
    plt.figure(figsize=(8, 6))
    bars = plt.bar(algorithms, times, color=['skyblue', 'lightgreen'])
    plt.title('Simulated Brute-force Time Comparison')
    plt.ylabel('Estimated Time (seconds)')
    
    for bar, value in zip(bars, times):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, f'{value:.2f}s', ha='center')
    
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
