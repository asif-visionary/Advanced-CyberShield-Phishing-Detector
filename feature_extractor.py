import re

def extract_url_features(url):
    domain = url.split("/")[2] if "://" in url else url.split("/")[0]
    return {
        "URLLength": len(url),
        "DomainLength": len(domain),
        "IsDomainIP": 1 if re.search(r"\d+\.\d+\.\d+\.\d+", url) else 0,
        "NoOfDegitsInURL": sum(c.isdigit() for c in url),
        "NoOfQMarkInURL": url.count("?"),
        "NoOfAmpersandInURL": url.count("&"),
        "NoOfOtherSpecialCharsInURL": sum(
            c in "@#$%^*(){}[]"
            for c in url
        ),
        "IsHTTPS": 1 if url.startswith("https") else 0
    }

def extract_email_features(text):
    text = str(text).lower()
    words = re.findall(r'\b\w+\b', text)
    
    num_words = len(words)
    num_unique_words = len(set(words))
    
    stopwords = {'the', 'is', 'in', 'at', 'of', 'on', 'and', 'a', 'to', 'for', 'it', 'with', 'as', 'by', 'this', 'that', 'from', 'your', 'you', 'are', 'be'}
    num_stopwords = sum(1 for w in words if w in stopwords)
    
    links = re.findall(r'(https?://[^\s]+)', text)
    num_links = len(links)
    
    domains = [re.sub(r'https?://', '', link).split('/')[0] for link in links]
    num_unique_domains = len(set(domains))
    
    emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    num_email_addresses = len(emails)
    
    urgent_keywords = {'urgent', 'suspended', 'verify', 'password', 'alert', 'immediate', 'action', 'required', 'account', 'update', 'login', 'security'}
    num_urgent_keywords = sum(1 for w in words if w in urgent_keywords)
    
    # Simplified spelling errors representation
    num_spelling_errors = 0 
    
    return {
        "num_words": num_words,
        "num_unique_words": num_unique_words,
        "num_stopwords": num_stopwords,
        "num_links": num_links,
        "num_unique_domains": num_unique_domains,
        "num_email_addresses": num_email_addresses,
        "num_spelling_errors": num_spelling_errors,
        "num_urgent_keywords": num_urgent_keywords
    }