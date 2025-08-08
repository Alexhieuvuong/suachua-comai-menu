#!/usr/bin/env python3
import os
from PIL import Image
import glob

def compress_image(input_path, output_path, quality=95, max_size=(1200, 1200)):
    """Compress an image while maintaining sharpness and quality"""
    try:
        with Image.open(input_path) as img:
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Resize if image is too large, but maintain aspect ratio
            if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Save with high quality compression
            img.save(output_path, 'JPEG', quality=quality, optimize=True, progressive=True)
            
            # Get file sizes
            original_size = os.path.getsize(input_path)
            compressed_size = os.path.getsize(output_path)
            reduction = ((original_size - compressed_size) / original_size) * 100
            
            print(f"✓ {os.path.basename(input_path)}: {original_size/1024:.1f}KB → {compressed_size/1024:.1f}KB ({reduction:.1f}% reduction)")
            
    except Exception as e:
        print(f"✗ Error processing {input_path}: {e}")

def main():
    # Create optimized directory
    optimized_dir = "optimized"
    if not os.path.exists(optimized_dir):
        os.makedirs(optimized_dir)
    
    # Get all image files
    image_files = glob.glob("*.png") + glob.glob("*.jpg") + glob.glob("*.jpeg")
    
    print("🖼️  Compressing images with high quality...")
    print("=" * 50)
    
    total_original = 0
    total_compressed = 0
    
    for image_file in image_files:
        if image_file.startswith("optimized_"):
            continue
            
        # Create output filename
        name, ext = os.path.splitext(image_file)
        output_file = os.path.join(optimized_dir, f"optimized_{name}.jpg")
        
        # Compress image
        original_size = os.path.getsize(image_file)
        total_original += original_size
        
        compress_image(image_file, output_file)
        
        compressed_size = os.path.getsize(output_file)
        total_compressed += compressed_size
    
    print("=" * 50)
    print(f"📊 Total size reduction: {total_original/1024/1024:.1f}MB → {total_compressed/1024/1024:.1f}MB")
    print(f"💾 Space saved: {((total_original - total_compressed) / total_original) * 100:.1f}%")
    print(f"📁 Optimized images saved in: {optimized_dir}/")
    print("\n✨ Images optimized with high quality - sharp and fast loading!")

if __name__ == "__main__":
    main()
