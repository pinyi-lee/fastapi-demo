import requests

url = 'https://ip-ranges.amazonaws.com/ip-ranges.json'
response = requests.get(url)
data = response.json()

cloudfront_ranges = [prefix['ip_prefix'] for prefix in data['prefixes'] if prefix['service'] == 'CLOUDFRONT']

with open('build/cloudfront_ranges.conf', 'w') as f:
    for ip_range in cloudfront_ranges:
        f.write(f"allow {ip_range};\n")
    f.write(f"deny all;\n")    

print("CloudFront IP ranges have been written to cloudfront_ranges.conf")
