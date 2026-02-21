# Olicyber Badge Generator (Fork)

This repository is a **personal fork** of the original [Olicyber Badge Generator](https://github.com/utcq/ocbadge).  

This fork introduces a few modifications for **privacy and convenience**, including:  
- Removal of personal information (username, nickname) from the badge.  
- Fixed the badge style to the “hacker” theme, no extra parameters required.  
- Automated badge generation without additional setup.  

---

## How It Works

### Authentication Token
- Log in to the [Training Platform](https://training.olicyber.it) and retrieve your token from the browser’s Local Storage, as in the original version.  
- Add it as a secret named `OC_TOKEN` in your repository settings (Settings → Secrets and variables → Actions).

### Badge Generation

**Automatic via GitHub Actions**  
- The workflow is configured to generate the badge **every hour**.  
- The badge is automatically saved as `card.svg` in the repository.

**Local Generation**  
```bash
export OC_TOKEN=*****
python3 gen.py