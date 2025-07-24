import requests

api_url = "http://127.0.0.1:5000/recommend"

# Use the 'data' parameter for form submissions (NOT 'json')
payload = {
    "query": "mobile app developer",
    "top_n": 3
}

response = requests.post(api_url, data=payload) # <--- Changed 'json=payload' to 'data=payload'

if response.status_code == 200:
    recommendations = response.json()
    print("Course Recommendations:")
    for course in recommendations:
        print(f"- Title: {course['title']}")
        print(f"  Platform: {course['platform']}")
        print(f"  Similarity Score: {course['similarity_score']:.4f}")
        print("-" * 20)
else:
    print(f"Error: {response.status_code} - {response.text}")