import re

# Read correct nav from privacy-policy.html
with open('privacy-policy.html', 'r', encoding='utf-8') as f:
    privacy_content = f.read()

# Extract from <nav class="navbar" id="navbar"> to </div>\n  </nav>
nav_match = re.search(r'<nav class="navbar" id="navbar">.*?</nav>', privacy_content, re.DOTALL)
# Extract from <div class="mobile-nav" id="mobileNav"> to </div>\n\n  <!-- Hero -->
mob_match = re.search(r'<div class="mobile-nav" id="mobileNav">.*?</div>', privacy_content, re.DOTALL)

if nav_match and mob_match:
    nav_str = nav_match.group(0)
    mob_str = mob_match.group(0)
    
    # swap active state in mobile nav
    mob_str = mob_str.replace('class="active">Privacy Policy', '>Privacy Policy')
    mob_str = mob_str.replace('>Terms of Service', ' class="active">Terms of Service')
    
    # Read terms-of-service.html
    with open('terms-of-service.html', 'r', encoding='utf-8') as f:
        tos_content = f.read()
        
    # In tos, find the starting point of the nav:
    # it was messed up and now looks like:
    # <p>Please read these terms carefully before using our website or engaging Vedtam Tech Solutions for any IT,
    
    # Wait, the best way to fix TOS is to read it, remove EVERYTHING from <nav class="navbar" id="navbar">
    # up to <!-- Hero -->
    # Since the previous replace deleted the <nav ...> tag, let's just find where it SHOULD be.
    
    # In the current terms-of-service.html, it has:
    # <body>
    #
    #         <p>Please read these terms carefully before using our website or engaging Vedtam Tech Solutions for any IT,
    
    # It deleted from <nav class="navbar" id="navbar"> all the way to <h1>Terms of Service</h1>.
    # Oh wow, it deleted the <h1>!
    
    # Find the start of the body content after the head
    body_start_match = re.search(r'</head>\s*<body>', tos_content, re.DOTALL)
    if not body_start_match:
        print("Error: Could not find <body> tag in terms-of-service.html")
        exit()
    
    # Find the start of the hero section to insert nav and mobile nav
    hero_section_start_match = re.search(r'<section class="hero legal-hero">', tos_content, re.DOTALL)
    if not hero_section_start_match:
        print("Error: Could not find hero section in terms-of-service.html")
        exit()

    # Reconstruct the file
    # Everything before the first <body> tag
    before_body = tos_content[:body_start_match.end()]
    
    # The content between <body> and the hero section
    between_body_and_hero = tos_content[body_start_match.end():hero_section_start_match.start()]

    # The rest of the content after the hero section
    after_hero = tos_content[hero_section_start_match.start():]

    new_tos_content = before_body + "\n" + nav_str + "\n" + mob_str + "\n" + after_hero

    with open('c:/Users/Manu/Desktop/vedtam website/terms-of-service.html', 'w', encoding='utf-8') as f:
        f.write(new_tos_content)
    print("Successfully fixed terms-of-service.html with updated nav and mobile nav.")
else:
    print("Error: Could not extract nav or mobile nav from privacy-policy.html")
