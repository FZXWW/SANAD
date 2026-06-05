# SANAD Invest AI - Public Deployment Guide

## Recommended Domain Names

Good options related to SANAD:

- `sanadinvest.ai`
- `sanad-invest.com`
- `sanadinvest.app`
- `sanadwealth.ai`
- `sanadadvisor.com`
- `sanadcapital.ai`
- `mysanadinvest.com`

Check availability before buying. My favorite choices are `sanadinvest.ai` for an AI-focused brand, or `sanad-invest.com` for a classic business domain.

## Best Hosting Option

Use Render or Railway because this is a Python Flask app with machine learning dependencies.

Recommended start command:

```bash
gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 300 --access-logfile -
```

One worker is intentional because the AI models train in memory. More workers would train duplicate model copies and use more RAM.

## Deploy on Render

1. Create a GitHub repository.
2. Upload this `sanad-web` folder to the repository.
3. In Render, create a new Web Service from the GitHub repo.
4. Use:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 300 --access-logfile -`
5. Wait for deployment to finish.
6. Open the temporary Render URL and test the form.

## Connect a Custom Domain

1. Buy one domain, for example `sanadinvest.ai`.
2. In the hosting platform, open the service settings and add a custom domain.
3. The platform will give you DNS records.
4. Add those records at your domain registrar.
5. Wait for DNS verification.
6. Enable HTTPS if the platform does not enable it automatically.

## Notes

- The first visit after deployment may take time because the AI models train once.
- Keep `datasets/`, `SA_Investment_Funds/`, and `SANAD_AI_FULL_SYSTEM.py` in the same deployed project.
- This project is educational and should show a disclaimer if used publicly as an investment tool.
