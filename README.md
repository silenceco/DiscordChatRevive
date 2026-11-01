# 💀 Discord Deadchat Bot

An asynchronous, lightweight Discord bot designed to keep server channels active. It monitors chat inactivity and automatically prompts the community with engaging, random questions when conversation slows down.

---

## 🔥 Key Features

- **Inactivity Monitoring:** Scans channel message history every 5 minutes to calculate inactivity duration.
- **Configurable Thresholds:** Easily adjust inactivity limits (e.g., 60 minutes) and automated check intervals.
- **Role Pings:** Automatically mentions a designated community role alongside the prompt to draw attention back to the chat.
- **Anti-Spam / Anti-Duplicate Logic:** Maintains an in-memory history of the last 5 asked questions to prevent repeat prompts.
- **Infinite Loop Protection:** Automatically skips execution if the last message in the channel was sent by the bot itself.

---

## 🛠️ How It Works

1. **Loop Check:** Every 5 minutes (`@tasks.loop(seconds=300)`), the bot fetches the most recent messages in the configured channel.
2. **Time Calculation:** It compares current UTC time against the timestamp of the last non-bot message.
3. **Threshold Evaluation:** If the calculated difference exceeds `INACTIVITY_MINUTES * 60` seconds, a revival prompt is triggered.
4. **Question Selection:** The bot filters out the last 5 asked questions, randomly picks an available question from the pool, updates its history buffer, and sends the prompt with a role ping.

---

## ⚙️ Requirements & Installation

### 1. Prerequisites
- **Python 3.8+** installed on your host system or VPS.
- A **Discord Bot Token** with `Message Content Intent` enabled in the [Discord Developer Portal](https://discord.com/developers/applications).

### 2. Dependencies
Install the required packages using `pip`:

```bash
pip install discord.py
