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

# Project cards (`ls ~/projects`), each linked to its repo. Facts come from
# each repo's own README. (name, repo, language, description, tags, live URL or "", status)
PROJECTS = [
    ("Gilli", "Gilli", "C#",
     "3D online Gilli-Danda. A C# engine with BEPU physics, compiled to WebAssembly, with "
     "peer-to-peer multiplayer over WebRTC and no game server.",
     ["C#", "WebAssembly", "Three.js", "TypeScript"], "https://gilli-rho.vercel.app", "play"),
    ("Snakes & Ladders 3D", "snake-and-ladder-", "TypeScript",
     "3D tabletop game with animated characters, snakes that bite and a real 3D die. "
     "Fully offline: every asset is generated procedurally.",
     ["React Three Fiber", "Three.js", "Vite"], "https://snakes-and-ladders-3d-psi.vercel.app", "play"),
    ("Fresora AI", "fresora-AI", "TypeScript",
     "Scan food, get a measured freshness score and use it before it's wasted. "
     "OpenCV + MobileNetV2 backend with an Expo app.",
     ["React Native", "FastAPI", "OpenCV"], "https://fresora-web.vercel.app", "live"),
    ("GrantPilot AI", "GrantPilot-Frontend", "JavaScript",
     "Grant and tender intelligence for Indian startups: discovery, bid-fit scoring, "
     "proposal and compliance workspaces.",
     ["React", "Vite", "Tailwind CSS"], "https://thanvanthat.github.io/GrantPilot-Frontend/", "live"),
    ("PatchPulse", "Patchpulse", "Python",
     "Turns player feedback from Steam, Discord and CSV into ranked themes, then traces "
     "complaint spikes to the release that caused them.",
     ["Python", "Postgres", "pgvector", "Redis"], "", "wip"),
    ("Portfolio", "portfolio", "TypeScript",
     "Cinematic portfolio built with Next.js, GSAP ScrollTrigger and React Three Fiber, "
     "with a case study for each project.",
     ["Next.js", "Tailwind CSS", "R3F"], "https://thanvanth.vercel.app", "live"),
    ("cinimatic", "cinimatic", "Unreal Engine",
     "A cinematic made with Unreal Engine.",
     ["Unreal Engine"], "", ""),
    ("Lumen Job Portal", "job-Appliction", "JavaScript",
     "Front-end job portal demo with job-seeker and employer roles, a light/dark theme "
     "and data kept in localStorage.",
     ["HTML", "CSS", "JavaScript"], "", ""),
    ("LeetCode Solutions", "leetcode-solutions", "C++",
     "LeetCode problems solved in C++.",
     ["C++"], "", ""),
]
