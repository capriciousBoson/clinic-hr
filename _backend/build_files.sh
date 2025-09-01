{
  "functions": { "backend/wsgi.py": { "runtime": "python3.12" } },
  "buildCommand": "bash ./build_files.sh",
  "outputDirectory": ".vercel/output",
  "routes": [
    { "src": "^/api/.*", "dest": "backend/wsgi.py" },
    { "src": "^/static/(.*)", "dest": "/static/$1" },
    { "src": "^(?!/api/).*", "dest": "/index.html" }
  ]
}
