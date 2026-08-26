# noBS_ServerAPI
REST API that links Discord accounts to Minecraft UUIDs.

## Backstory
I own a Minecraft server with website, login page and statistics page. Login is implemented using discord, since it was easy to do using DiscordSRV.
It was all done using nginx - just sharing full on raw file with discord accounts beside the minecraft UUIDs, the same thing with statistics file. 
This API changes this "duct tape" in my server infrastructure for a proper, I would say, welding.

## Architecture
To avoid opening ports on my homelab server, everything is tunneled through Azure using Tailscale. That way Azure becomes the only public attack surface, while also keeping my real IP hidden. Azure receives data from the Minecraft server over the Tailscale which then is consumed by Node.js frontend built by another developer.
Example:
Player -> Site -> API on Azure -> synced data from Minecraft server via Tailscale

## API Endpoints

### Linking Discord account and Minecraft account
```GET /accounts/{discord_id}```

Takes Discord ID, checks if a matching account exists, and returns the linked Minecraft player UUID.

### Getting all statistics
```GET /stats/all```

Returns all existing statistics

### Getting statistics of a player
```GET /stats/player/uuid/{uuid}```

Takes UUID, checks if a matching account exists, and returns all the stats of the player.

### Getting specific statistic of a player
```GET /stats/player/uuid/{uuid}/{stat_name}```

Takes UUID and statistic name, checks if a matching account exists and if statistic name exists, and returns specific statistics value of the player.

### Getting players stats by player name
```GET /stats/player/name/{player_name}```

Takes player name, checks if matching account exists, and returns all statistics of the player.

### Getting death_rate value of all players
```GET /stats/metrics/death_rate```

Calculates and returns players death rate.

### Getting total_hours value of all players
```GET /stats/metrics/total_hours```

Calculates and returns total hours played by all players.

### Getting current server online
```GET /online```

Provides online players.

### Getting latest channel message
```GET /get_message```

Returns the latest Telegram channel message converted to markdown.

### Getting image
```GET /get_image/{date}```

Returns image made on given date.

### Receiving converted telegram message
```POST /receive_message```

Requires an auth token and does two things:
 1. Receives message in dict format from telegram bot and writes it to a json file. 
 2. Creates a path for a message image and also writes it to a json file.

## Tech Stack

- Python (FastAPI) - API framework
- Azure VM - hosting
- Tailscale - encrypted tunnel between Azure and home server
- Docker

## API url demo
### Api docs
https://api.noboobs.world/docs

### Accounts link
https://api.noboobs.world/accounts/934533956244742194

### Statistics
https://api.noboobs.world/stats/player/uuid/0c1f6b90-3499-3393-9ec2-412a4ba68884

### Online
https://api.noboobs.world/online

## Related repos
- [Telegram Bot](https://github.com/Sl0wYx/noBS_BotIntegrator)
- [Infrastructure](https://github.com/Sl0wYx/noBS_Infrastructure)
