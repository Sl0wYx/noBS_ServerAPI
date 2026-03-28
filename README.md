# noBS_ServerAPI
REST API that links Discord accounts to Minecraft UUIDs.

## Backstory
I own a Minecraft server with website, login page and statistics page. Login is implemented using discord, since it was easy to do using DiscordSRV.
It was all done using nginx - just sharing full on raw file with discord accounts beside the minecraft UUIDs, the same thing with statistics file. 
This API changes this "ducktape" in my server infrastructure for a proper, I would say, welding.

## Architecture
To avoid opening ports on my homelab server, everything is tunneled through Azure using Tailscale. Azure receives data from the Minecraft server over the Tailscale which then is consumed by Node.js frontend build by another developer.
Example:
Player -> Site -> API on Azure -> synced data from Minecraft server via Tailscale

## API Endpoints

### Linking Discord account and Minecraft account
```GET /accounts/{discord_id}```

Takes a Discord ID, checks if a matching account exists, and returns the linked Minecraft player UUID.

Example request:
```GET /accounts/934533956244742194```

Example response:
```{"DiscordID": 934533956244742194, "PlayerUUID": "32337244-5a74-3143-aa78-ce6736d8f490"}```

If the ID is not found:
```404 Account with that ID does not exist```

### Getting all statistics
```GET /stats/all```

Reads file stats.json

Example response:
```{"Distance Fallen":{"demoralize":"50267","Anfox":"7371065",...}}```

### Getting statistics of a player
```GET /stats/{uuid}```

Takes a UUID, checks if a matching account exists, and returns all the stats of the player.

Example request:
```GET stats/0c1f6b90-3499-3393-9ec2-412a4ba68884```

Example response:
```{"uuid":"0c1f6b90-3499-3393-9ec2-412a4ba68884","Hoppers Inspected":"23"...}```

If the ID is not found:
```404 Account with that uuid not found```

### Getting specific statistic of a player
```GET /stats/{uuid}/{stat_name}```

Takes a UUID and statistic name, checks if a matching account exists and if statistic name exists, and returns specific statistic value the stats of the player.

Example request:
```GET stats/0c1f6b90-3499-3393-9ec2-412a4ba68884/Hoppers Inspected```

Example response:
```{"uuid":"0c1f6b90-3499-3393-9ec2-412a4ba68884","Player Name":"Example","Hoppers Inspected":"23"}```

If the ID is not found:
```404 Stats not found```

### Getting current server online
```GET /online```

Provides online players.

Example request:
```GET /online```

Example response:
```["7a20cf2d-9161-3db5-9d3c-31b2a661a0e5","9ec01599-d8a8-3853-b93e-43ad6e1258cc"]```

### Getting latest channel message
```GET /get_message```

Returns the latest Telegram channel message converted to markdown.
Example response:
```{"Message": "**Announcement title**\nAnnouncement body", "Date": "2026-03-26 00:37:46", "Image": "<image url>"}```

### Getting image
```GET /get_image/{date}```

Returns image made on given date.

Example response:
```{image}```

## Tech Stack

- Python (FastAPI) - API framework
- Azure VM - hosting
- Tailscale - encrypted tunnel between Azure and home server
- Docker

## API url demo
### Accounts link
https://api.noboobs.world/accounts/934533956244742194

### Statistics
https://api.noboobs.world/stats/0c1f6b90-3499-3393-9ec2-412a4ba68884

### Online
https://api.noboobs.world/online

## Related repos
- [Telegram Bot](https://github.com/Sl0wYx/noBS_BotIntegrator)
- [Infrastructure](https://github.com/Sl0wYx/noBS_Infrastructure)
