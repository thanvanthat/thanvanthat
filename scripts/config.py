"""Shared settings for the profile-art scripts. Edit these to make it yours."""

USERNAME = "thanvanthat"          # GitHub login whose contributions are drawn
HANDLE = "thanvanth@github"       # shown in the info-card title bar
INITIALS = "TA"                   # ASCII fallback when no photo is provided

# Neofetch-style card rows: (key, value). Keep the story here; the
# contribution graph already covers the GitHub stats.
INFO_ROWS = [
    ("Name", "Thanvanth AT"),
    ("Role", "Student @ SNS College of Technology"),
    ("Goal", "Aspiring Game Developer"),
    ("Loc", "Trichy, India"),
    ("Stack", "C++ · TypeScript · JavaScript"),
    ("Engine", "Unreal Engine"),
    ("", ""),
    ("Built", "Fresora AI · GrantPilot"),
    ("", "board-app · cinimatic (Unreal)"),
    ("", "LeetCode solutions in C++"),
    ("", ""),
    ("Social", "@thanvanth_ox"),
]

# Lines the headline types out, one after another, on a loop.
HEADLINE = [
    "Hi, I'm Thanvanth",
    "Aspiring Game Developer",
    "C++ · Unreal Engine · TypeScript",
    "Building Fresora AI & GrantPilot",
]

# Tech-stack badge rows: (category, [(label, simple-icons slug), ...]).
# Icons come from scripts/icons.json (Simple Icons, CC0).
STACK = [
    ("languages", [("C++", "cplusplus"), ("TypeScript", "typescript"), ("JavaScript", "javascript"),
                   ("Python", "python"), ("HTML5", "html5"), ("CSS", "css")]),
    ("frontend", [("React", "react"), ("Tailwind CSS", "tailwindcss"), ("Vite", "vite")]),
    ("mobile", [("React Native", "react"), ("Expo", "expo")]),
    ("backend", [("FastAPI", "fastapi"), ("Supabase", "supabase"), ("Vercel", "vercel")]),
    ("gamedev", [("Unreal Engine", "unrealengine")]),
    ("tools", [("Git", "git"), ("GitHub", "github")]),
]

# Connect badges: (file name, label, simple-icons slug, link).
SOCIALS = [
    ("github", "GitHub", "github", "https://github.com/thanvanthat"),
    ("instagram", "Instagram", "instagram", "https://instagram.com/thanvanth_ox"),
    ("email", "Email", "gmail", "mailto:thanvanthat24@gmail.com"),
]

# Featured project panel (facts from the project's own README).
FEATURED = {
    "name": "Fresora AI",
    "path": "~/projects/fresora-ai",
    "tagline": "AI-assisted food freshness & zero-waste assistant",
    "pipeline": ["SCAN", "IDENTIFY", "MEASURE", "SCORE", "RECOMMEND", "TRACK", "RESCUE"],
    "bullets": [
        "Measures the food surface with OpenCV: dark defects, colour consistency, hue drift, texture",
        "Scores freshness 0-100 with a documented, deterministic formula, from Fresh to Spoiled",
        "Identifies food with MobileNetV2 on ONNX Runtime: no TensorFlow, nothing to download",
        "Zero-waste recipes that use what's about to spoil first, never anything assessed as spoiled",
        "One React Native codebase: a 27-screen Expo app that also ships to the web",
    ],
    "tags": ["TypeScript", "React Native", "Expo", "FastAPI", "OpenCV", "ONNX Runtime", "Supabase", "Vercel"],
    "links": [("Live app", "https://fresora-web.vercel.app"),
              ("Repo", "https://github.com/thanvanthat/fresora-AI")],
}
