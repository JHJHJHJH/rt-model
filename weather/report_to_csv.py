import xml.etree.ElementTree as ET
import csv
import re
from datetime import datetime
import os
import glob
import zipfile
import tempfile
import shutil

def parse_rss_weather_data(xml_content, filename=""):
    """Parse RSS weather data from XML content"""
    try:
        root = ET.fromstring(xml_content)
    except ET.ParseError:
        return None
    
    item = root.find('.//item')
    if item is None:
        return None
    
    # Extract publication date
    pub_date_element = item.find('pubDate')
    pub_date = pub_date_element.text.strip() if pub_date_element is not None else ''
    
    # Parse the date
    try:
        dt = datetime.strptime(pub_date, '%a, %d %b %Y %H:%M:%S GMT')
        formatted_date = dt.strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        formatted_date = pub_date
    
    # Extract description content
    description_element = item.find('description')
    if description_element is None or description_element.text is None:
        return None
    
    description_text = description_element.text
    
    # Extract relative humidity
    humidity = None
    humidity_pattern = r'Relative Humidity : (\d+) per cent'
    humidity_match = re.search(humidity_pattern, description_text)
    if humidity_match:
        humidity = humidity_match.group(1)
    
    # Extract station data
    stations_data = []
    station_pattern = r'<tr><td><font size="-1">([^<]+)</font></td><td[^>]*><font size="-1">([\d]+) degrees'
    station_matches = re.findall(station_pattern, description_text)
    
    if not station_matches:
        return None
    
    for station_name, temperature in station_matches:
        station_name = station_name.strip()
        if station_name.endswith((';', '.')):
            station_name = station_name[:-1].strip()
        
        stations_data.append({
            'datetime': formatted_date,
            'station_name': station_name,
            'temperature': temperature,
            'humidity': humidity,
            'source_zip': '',
            'source_xml': os.path.basename(filename)
        })
    
    return stations_data

def process_zip_file(zip_path, temp_dir):
    """Process a single zip file"""
    all_data = []
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
            
            # Find all XML files recursively
            xml_files = []
            for root_dir, _, files in os.walk(temp_dir):
                for file in files:
                    if file.lower().endswith('.xml'):
                        xml_files.append(os.path.join(root_dir, file))
            
            for xml_file in xml_files:
                try:
                    with open(xml_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    data = parse_rss_weather_data(content, xml_file)
                    if data:
                        # Add zip file info to each record
                        zip_name = os.path.basename(zip_path)
                        for record in data:
                            record['source_zip'] = zip_name
                        all_data.extend(data)
                        
                except Exception as e:
                    print(f"Error processing {xml_file}: {e}")
    
    except Exception as e:
        print(f"Error processing zip {zip_path}: {e}")
    
    return all_data

def process_zip_folder(folder_path, zip_pattern="*.zip"):
    """Process all zip files in a folder"""
    all_data = []
    zip_files = glob.glob(os.path.join(folder_path, zip_pattern))
    
    if not zip_files:
        print(f"No zip files found in {folder_path}")
        return all_data
    
    print(f"Found {len(zip_files)} zip files to process")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        for zip_file in zip_files:
            print(f"Processing: {os.path.basename(zip_file)}")
            data = process_zip_file(zip_file, temp_dir)
            if data:
                all_data.extend(data)
                print(f"  Extracted {len(data)} records")
            
            # Clean temp directory for next file
            for item in os.listdir(temp_dir):
                item_path = os.path.join(temp_dir, item)
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path, ignore_errors=True)
                else:
                    os.remove(item_path)
    
    return all_data

def save_to_csv(data, output_file):
    """Save data to CSV"""
    if not data:
        return False
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['datetime', 'station_name', 'temperature', 'humidity', 'source_zip', 'source_xml'])
        writer.writeheader()
        writer.writerows(data)
    
    return True

ZIP_FOLDER = "./weather/data/weather-reports"  
OUTPUT_CSV = "./weather/data/daily_weather.csv" 
ZIP_PATTERN = "*.zip" 

if __name__ == "__main__":
    if os.path.exists(ZIP_FOLDER):
        print(f"Processing zip files from: {ZIP_FOLDER}")
        weather_data = process_zip_folder(ZIP_FOLDER, ZIP_PATTERN)
        
        if weather_data:
            print(f"\nSuccessfully extracted {len(weather_data)} records")
            
            if save_to_csv(weather_data, OUTPUT_CSV):
                print(f"Data saved to: {OUTPUT_CSV}")
                
                # Show summary
                unique_zips = len(set(d['source_zip'] for d in weather_data))
                unique_stations = len(set(d['station_name'] for d in weather_data))
                print(f"From {unique_zips} zip files, {unique_stations} unique stations")
            else:
                print("Failed to save CSV")
        else:
            print("No data extracted")
    else:
        print(f"Folder '{ZIP_FOLDER}' does not exist")