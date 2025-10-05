# TDS_Week2_Vercel
## Telemetry API

This is a Python endpoint to calculate per-region metrics from telemetry data.  

## Deployment

1. Install Vercel CLI: `npm i -g vercel`
2. Login: `vercel login`
3. Deploy: `vercel --prod`

## Usage

POST to `/api/telemetry` with JSON body:

```json
{
  "regions": ["emea", "apac"],
  "threshold_ms": 186
}
