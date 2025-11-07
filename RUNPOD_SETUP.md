# RunPod Setup Guide

## Current Status
✅ API is running on port 8000  
✅ CORS enabled for internet access  
✅ Ready to accept external requests

## Getting Your Public URL

### Option 1: RunPod Public IP (Recommended)
1. Go to your RunPod pod dashboard
2. Look for the **Public IP** or **Connect** section
3. Your API URL will be: `http://PUBLIC_IP:8000`

### Option 2: RunPod Port Mapping
If RunPod shows a mapped port (e.g., 12345 → 8000):
- Your API URL: `http://PUBLIC_IP:12345`

### Option 3: Check from Inside the Pod
Run this command in the pod terminal:
```bash
curl ifconfig.me
```
This gives you the public IP. Your API URL: `http://THAT_IP:8000`

## Testing External Access

Once you have your public URL, test it:

```bash
# Health check
curl http://YOUR_PUBLIC_IP:8000/

# Search test
curl -X POST http://YOUR_PUBLIC_IP:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "البخاري", "top_n": 3}'
```

## Firewall / Port Configuration

Make sure port **8000** is:
- ✅ Open in RunPod firewall settings
- ✅ Exposed in your pod configuration
- ✅ Not blocked by network policies

## Update Integration Guide

Once you have your public URL:
1. Open `INTEGRATION_GUIDE.md`
2. Replace all instances of `YOUR_RUNPOD_URL` with your actual URL
3. Share with your integration team

Example:
```
Before: http://YOUR_RUNPOD_URL:8000
After:  http://123.45.67.89:8000
```

## Verification Checklist

- [ ] API responds to `http://PUBLIC_IP:8000/` with `{"status":"ok"}`
- [ ] Search endpoint works from external network
- [ ] Interactive docs accessible at `http://PUBLIC_IP:8000/docs`
- [ ] CORS allows requests from your frontend (if applicable)

## Current Service

The API is running in the background. To check status:
```bash
curl http://localhost:8000/
```

To view logs:
```bash
ps aux | grep "python main.py"
```

To restart if needed:
```bash
cd /workspace/arabic_rag_api
source venv/bin/activate
pkill -f "python main.py"
python main.py &
```

---

**Next Step**: Find your public IP/URL and update the integration guide!

