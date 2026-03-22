# noBS_AccountAPI
REST API that links Discord accounts to Minecraft UUIDs.

## Backstory
I own a Minecraft server with website and login page. Login is implemented using discord, since it was easy to do using DiscordSRV.
It was all done using nginx - just sharing full on raw file with discord accounts beside the minecraft UUIDs. 
This API changes this "ducktape" in my server infrastructure for a proper, I would say, welding.

## Architecture
To avoid opening ports on my homelab server, everything is tunneled through Azure using Tailscale. Azure receives synced data from the Minecraft server over the Tailscale which then is consumed by Node.js frontend build by another developer.
Example:
Player -> Site -> API on Azure -> synced data from Minecraft server via Tailscale

## API Endpoint

```GET /accounts/{discord_id}```

Takes a Discord ID, checks if a matching account exists, and returns the linked Minecraft player UUID.

Example request:
```GET /accounts/934533956244742194```

Example response:
```{"DiscordID": 934533956244742194, "PlayerUUID": "32337244-5a74-3143-aa78-ce6736d8f490"}```

If the ID is not found:
```{"Error": "Account with that ID does not exist"}```

## Tech Stack

- Python (FastAPI) - API framework
- Azure VM - hosting
- Tailscale - encrypted tunnel between Azure and home server

## API url demo
https://api.noboobs.world/accounts/934533956244742194
