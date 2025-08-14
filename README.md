# MSCHelper Discord Bot

This is a comprehensive Discord bot designed to enhance server moderation, manage user roles, and provide utility features.

## Features

The bot includes the following key functionalities:

### 1. Anti-Scam System (`src/cogs/AntiScam.py`)
- **Scam Message Detection**: Utilizes a machine learning model to identify and delete messages containing scam attempts.
- **Suspicious Link Blocking**: Automatically detects and removes messages with suspicious links.
- **User Timeout**: Temporarily mutes users who send scam messages or suspicious links.
- **Webhook Notifications**: Sends alerts to a designated webhook channel for detected scam activities.

### 2. Anti-Spam System (`src/cogs/Antispam.py`)
- **General Spam Detection**: Monitors message frequency to prevent rapid-fire spam.
- **Duplicate Message Detection**: Identifies and acts upon repeated messages (copy-paste spam).
- **Spotify Spam Prevention**: Detects and handles spam related to Spotify links, RPC, and embeds.
- **Configurable Thresholds**: Administrators can set custom limits for various spam types using slash commands (`/set_spam_threshold`, `/set_duplicate_threshold`, `/set_spotify_threshold`).
- **Automated Punishment**: Deletes spam messages and applies timeouts to spammers.
- **Webhook Logging**: Logs all detected spam incidents to a webhook channel.

### 3. Discord Link Detection (`src/cogs/DiscordLinkDetection.py`)
- **Invite Link Blocking**: Automatically deletes messages containing Discord invite links to prevent unauthorized advertising.
- **General Discord Advertising Prevention**: Blocks messages that attempt to advertise other Discord servers.
- **Edit Monitoring**: Catches and deletes invite/advertising links even if they are added via message edits.

### 4. Auto-Pinger (`src/cogs/autoping.py`)
- **New Member Pings**: Pings newly joined members in specified channels after a short delay, welcoming them to the server.

### 5. Unified Moderation System (`src/cogs/moderation.py`)
- **Mute/Unmute Commands**: Allows moderators to timeout and remove timeouts from users (`/mute`, `/unmute`).
- **Ban Request System**: Provides a form-based system (`/form-ban`) for moderators to request user bans, which can then be approved or denied by senior moderators via interactive buttons.
- **Direct Ban Command**: Senior moderators can directly ban users (`/ban`).
- **Moderator Management**: Commands to add and remove moderator roles (`/moder-add`, `/moder-remove`).
- **Reprimand System**: Implements a warning system for moderators (`/vig-add`, `/vig-remove`). Accumulating three reprimands automatically removes the moderator role.
- **Comprehensive Logging**: All moderation actions are logged to dedicated channels.
- **Error Handling**: Robust error handling for permissions, user not found, and command cooldowns.
- **SQLite Database**: Uses an SQLite database to persist moderator reprimand counts.

### 6. MSC Friends Verification (`src/cogs/mscfriends.py`)
- **Role Verification**: Assigns a special "verified" role to users who meet specific criteria (e.g., having "discord.gg/pon" in their custom status or "ᵐˢᶜ" in their global name).
- **Periodic Re-verification**: Regularly checks if verified users still meet the criteria and removes the role if they don't.
- **Interactive Verification**: Provides a user-friendly verification process with language selection and a "Check" button.

### 7. Private Voice Channels (`src/cogs/privatevoices.py`)
- **Dynamic Channel Creation**: Users automatically get a private voice channel when they join a designated "creator channel".
- **Automatic Deletion**: Private channels are automatically deleted when they become empty.
- **Control Panel**: Owners of private voice channels can manage their rooms using an interactive panel with options for:
    - **User Limit**: Set the maximum number of participants.
    - **Kick User**: Remove specific users from the channel.
    - **Visibility**: Make the channel visible or hidden to others.
    - **Lock/Unlock**: Restrict or allow entry to the channel.
    - **Access Control**: Grant, revoke, or reset individual user permissions for the channel.
- **Multi-language Support**: The control panel supports both Russian and English.

## Installation

### Prerequisites
- Python 3.13+
- `uv` (a fast Python package installer and resolver)
- Docker and Docker Compose (optional, for containerized deployment)

### Local Setup (using `uv`)

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/xdearboy/mscbots-main.git
    cd mscbots-main/MSCHelper
    ```

2.  **Install `uv`:**
    If you don't have `uv` installed, you can install it via `pip`:
    ```bash
    pip install uv
    ```

3.  **Install dependencies:**
    ```bash
    uv sync
    ```

### Docker Setup

1.  **Ensure Docker and Docker Compose are installed.**

2.  **Navigate to the project root:**
    ```bash
    cd mscbots-main/MSCHelper
    ```

3.  **Build and run the Docker containers:**
    ```bash
    docker-compose up --build
    ```
    This will build the Docker image and start the bot.

## Usage

### Bot Token
The bot requires a Discord bot token to run. You need to **directly replace the placeholder token in `main.py`** with your actual bot token.

Open `main.py` and change the line:
```python
token = "token"
```
to:
```python
token = "YOUR_ACTUAL_BOT_TOKEN_HERE"
```
**Warning**: Hardcoding your bot token directly in the code is generally not recommended for security reasons. For production environments, consider using environment variables or a secure configuration management system.

### Running the Bot

#### Locally (using `uv`)
After replacing the token in `main.py` and installing dependencies:
```bash
uv run main.py
```

#### With Docker Compose
After replacing the token in `main.py` and building the containers:
```bash
docker-compose up
```
To run in detached mode (in the background):
```bash
docker-compose up -d
```

### Commands
The bot primarily uses **slash commands** (e.g., `/mute`, `/set_spam_threshold`). You can find a list of available commands and their descriptions by typing `/` in your Discord server where the bot is active.
