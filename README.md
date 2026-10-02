# SmartNoise | Noise awareness and monitoring prototype

SmartNoise is a static browser application for learning about noise exposure, tracking local demo readings, and preparing community incident reports. It is an educational prototype, not a calibrated sound meter, clinical tool, government service, or backend account platform.

## Start here

Serve this directory from HTTPS or localhost and open `index.html`. Visitors are directed to `login.html`; after signing in, the protected application opens at `dashboard.html`.

## Application areas

- Dashboard, microphone estimate and clearly marked simulated Demo Mode
- Analytics, local history and CSV export
- Noise zones, controls, limits and community reporting
- Awareness center: hearing-health guidance, CDC/NIOSH videos, WHO/CDC resources, exposure example calculator and report checklist
- Research & Learning Desk: newspaper-style research notes, study guide and original illustrations
- Team page and project credits for Prince Jainwar
- Profile, reports, notifications, settings, country and language preferences

## Important limitations

Accounts and reports are stored only in the current browser. There is no server-side authentication, account recovery, email delivery, cross-device sync, official complaint submission, or actual city-sensor connection. Browser-only route guards control the interface but cannot provide authorization for data hosted on a public static server.

The app's working interface translations are currently English, Hindi, Spanish, French, German, Portuguese, and Japanese, with the broadest translated coverage on the login, shared navigation, and awareness headings. Some detailed page content and dynamic messages remain English. Do not treat language preferences as complete translation coverage. The Research & Learning Desk is currently in English.

The occupational NIOSH 85 dBA / 8-hour value is shown only as a workplace reference. The educational dose widget is not personal risk assessment or a legal compliance result. SmartNoise microphone estimates are not calibrated dBA measurements.

## Run and rebuild

Open this directory in a local static web server. To rebuild the generated HTML from source, run `python tools/build.py` from this folder. `tools/smoke.js` is the dashboard-script smoke check.

## Verified health references

- WHO safe listening: https://www.who.int/news-room/questions-and-answers/item/deafness-and-hearing-loss-safe-listening
- WHO environmental noise: https://www.who.int/tools/compendium-on-health-and-environment/environmental-noise/
- CDC/NIOSH hearing loss: https://www.cdc.gov/niosh/noise/about/noise.html
- CDC/NIOSH prevention: https://www.cdc.gov/niosh/noise/prevent/
