# RunPod Port Exposure Guide

## Current Issue
Your API is running internally on port 8000, but it's not accessible from the internet because the port isn't exposed through RunPod's firewall.

## ⚡ Quick Fix: Expose Port in RunPod Dashboard

### Step 1: Access RunPod Dashboard
1. Go to https://www.runpod.io/console/pods
2. Find your pod: **kaohoz7ihe09do** (hostname: kaohoz7ihe09do-64411de1)

### Step 2: Expose the Port
**Look for one of these sections:**
- "Exposed Ports"
- "TCP Port Mappings"  
- "Port Forwarding"
- Or a button like "+ Expose Port" / "Connect" / "Ports"

### Step 3: Add Port Mapping
**Add this port:**
- **Internal Port**: `8001` 
- **Type**: HTTP or TCP
- Click "Save" or "Add"

RunPod will assign a public port (example: `8001 → 54321`)

### Step 4: Update Your API URL
Once exposed, your API URL will be:
```
http://203.57.40.119:PUBLIC_PORT/search
```

Where `PUBLIC_PORT` is the port RunPod assigned (you'll see it in the dashboard).

---

## 🔍 Where to Find Port Settings

### Option A: On Pod Page
- Click on your pod name
- Look for a "Connect" or "Ports" tab
- Should show current port mappings (SSH is already mapped: 22→10191)

### Option B: In Pod Settings
- Click the gear/settings icon on your pod
- Look for "Network" or "Ports" section
- Add port 8001 (or 8000)

### Option C: Pod Details Panel
- When viewing pod details, check right sidebar
- May have "Exposed Ports" section with "+ Add Port" button

---

## 📝 What to Expose

**Recommended**: Expose port **8001**
- RunPod already has nginx configured to proxy 8001 → 8000
- Your API runs on 8000, nginx forwards from 8001

**Alternative**: Expose port **8000** directly
- Will work, but 8001 is already set up with nginx proxy

---

## ✅ After Exposing Port

### Test Connection
Once you've exposed the port and got the public port number, test:

```bash
# Replace XXXXX with your assigned public port
curl http://203.57.40.119:XXXXX/

# Should return: {"status":"ok"}
```

### Full Test
```bash
curl -X POST http://203.57.40.119:XXXXX/search \
  -H "Content-Type: application/json" \
  -d '{"query": "البخاري", "top_n": 3}'
```

### Update Documentation
Once working, update these files with your actual public port:
- `INTEGRATION_GUIDE.md`
- `SHARE_WITH_TEAM.txt`

Replace `8001` with your assigned public port throughout.

---

## 🆘 If You Can't Find Port Settings

### Check Pod Type
Some RunPod pod types have different interfaces:
- **Community Cloud**: Usually has easy port exposure
- **Secure Cloud**: May require support ticket
- **On-Demand vs Spot**: Interface may differ

### Alternative: Use RunPod's Proxy URL
Some RunPod templates provide HTTP endpoints like:
- `https://YOUR_POD_ID-8000.proxy.runpod.net`
- Check your pod details for any "Public URL" field

### Contact RunPod Support
If you can't expose ports:
1. Go to RunPod Support/Help
2. Ask: "How do I expose port 8001 for my pod?"
3. Provide Pod ID: `kaohoz7ihe09do`

---

## 🔐 Current Port Status

**Currently Exposed:**
- SSH Port 22 → Public Port 10191 ✅

**Need to Expose:**
- HTTP Port 8001 → Public Port ??? ⏳

**Your API:**
- Running internally on port 8000 ✅
- Nginx proxying 8001 → 8000 ✅
- Waiting for external access ⏳

---

**Next Step**: Expose port 8001 in RunPod dashboard, then test with the assigned public port!

