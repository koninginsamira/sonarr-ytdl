# sonarr-ytdl (a fork of sonarr_youtubedl by [@whatdaybob](https://github.com/whatdaybob))
[![pipeline status](https://gitlab.com/FoxAmes/sonarr-ytdl/badges/main/pipeline.svg)](https://gitlab.com/FoxAmes/sonarr-ytdl/-/commits/main) 

This fork is to address some outstanding issues with the upstream that have gone unaddressed for some time:
- Issue triggering rescans [#52](https://github.com/whatdaybob/sonarr_youtubedl/pull/52)
- yt-dlp update [#32](https://github.com/whatdaybob/sonarr_youtubedl/issues/32)
  - Broken extractions resulted from this [#54](https://github.com/whatdaybob/sonarr_youtubedl/issues/54)
- Subtitles are all downloaded, ignoring whitelisted languages [cause at time of writing](https://github.com/whatdaybob/sonarr_youtubedl/blob/3d3b1d55c6799cc3f317d08639b9a60cd41c64d9/app/sonarr_youtubedl.py#L395)
- Rebase on alpine to slim down image size and reduce unnecessary image content

**I will likely not do a great job of maintaining this fork**, but I will try to be responsive to PRs and issues as they crop up.

You can pull these images straight from GitLab's Container registry: `registry.gitlab.com/foxames/sonarr-ytdl/sonarr-ytdl`.

# Old README

[whatdaybob/sonarr_youtubedl](https://github.com/whatdaybob/Custom_Docker_Images/tree/master/sonarr_youtubedl) is a [Sonarr](https://sonarr.tv/) companion script to allow the automatic downloading of web series normally not available for Sonarr to search for. Using [YT-DLP](https://github.com/yt-dlp/yt-dlp) (a youtube-dl fork with added features) it allows you to download your webseries from the list of [supported sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md).

## Features

* Downloading **Web Series** using online sources normally unavailable to Sonarr
* Ability to specify the downloaded video format globally or per series
* Downloads new episodes automatically once available
* Imports directly to Sonarr and it can then update your plex as and example
* Allows setting time offsets to handle prerelease series
* Can pass cookies.txt to handle site logins

## How do I use it

Firstly you need a series that is available online in the supported sites that YouTube-DL can grab from.
Secondly you need to add this to Sonarr and monitor the episodes that you want.
Thirdly edit your config.yml accordingly so that this knows where your Sonarr is, which series you are after and where to grab it from.
Lastly be aware that this requires the TVDB to match exactly what the episodes titles are in the scan, generally this is ok but as its an openly editable site sometime there can be differences.

## Supported Architectures

The architectures supported by this image are:

| Architecture | Tag |
| :----: | --- |
| x86-64 | latest |
| x86-64 | dev |

## Version Tags

| Tag | Description |
| :----: | --- |
| latest | Current release code |
| dev | Pre-release code for testing issues |

## Great how do I get started

Obviously its a docker image so you need docker, if you don't know what that is you need to look into that first.

### docker

```bash
docker create \
  --name=sonarr_youtubedl \
  -v /path/to/data:/config \
  -v /path/to/sonarrmedia:/sonarr_root \
  -v /path/to/logs:/logs \
  --restart unless-stopped \
  whatdaybob/sonarr_youtubedl
```

### docker-compose

```yaml
---
version: '3.4'
services:
  sonarr_youtubedl:
    image: whatdaybob/sonarr_youtubedl
    container_name: sonarr_youtubedl
    volumes:
      - /path/to/data:/config
      - /path/to/sonarrmedia:/sonarr_root
      - /path/to/logs:/logs
```

### Docker volumes

| Parameter | Function |
| :----: | --- |
| `-v /config` | sonarr_youtubedl configs |
| `-v /sonarr_root` | Root library location from Sonarr container |
| `-v /logs` | log location |

**Clarification on sonarr_root**

A couple of people are not sure what is meant by the sonarr root. As this downloads directly to where you media is stored I mean the root folder where sonarr will place the files. So in sonarr you have your files moving to `/mnt/sda1/media/tv/Smarter Every Day/` as an example, in sonarr you will see that it saves this series to `/tv/Smarter Every Day/` meaning the sonarr root is `/mnt/sda1/media/` as this is the root folder sonarr is working from.

## Configuration file

On first run the docker will create a template file in the config folder. Example [config.yml.template](./app/config.yml.template)

Copy the `config.yml.template` to a new file called `config.yml` and edit accordingly.
