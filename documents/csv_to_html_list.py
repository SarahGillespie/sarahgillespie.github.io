import csv

# Read the CSV file
input_file = 'MyEBirdData.csv'  # Replace with your CSV filename
output_file = 'output.html'

# Set to track unique pairs
seen_pairs = set()
unique_entries = []

# Open and read the CSV
with open(input_file, 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    
    # Collect unique pairs
    for row in reader:
        common_name = row['Common Name'].strip()
        scientific_name = row['Scientific Name'].strip()
        
        # Create a tuple for tracking uniqueness
        pair = (common_name, scientific_name)
        
        # Only add if we haven't seen this pair before
        if pair not in seen_pairs:
            seen_pairs.add(pair)
            unique_entries.append(pair)

# Sort entries alphabetically by common name
unique_entries.sort(key=lambda x: x[0].lower())

# Write unique entries to file
with open(output_file, 'w', encoding='utf-8') as outfile:
    for common_name, scientific_name in unique_entries:
        html_line = f"          <li>{common_name} ({scientific_name})</li>\n"
        outfile.write(html_line)

print(f"HTML list items have been written to {output_file}")
print(f"Total unique entries: {len(unique_entries)}")

# Print to console
print("\nOutput:")
for common_name, scientific_name in unique_entries:
    print(f"          <li>{common_name} ({scientific_name})</li>")