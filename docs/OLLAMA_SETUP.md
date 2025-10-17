# Ollama Setup Guide for AI Feedback

## Overview
This guide explains how to set up Ollama with the Mistral model to enable AI-powered feedback in the fleet dashboard.

## Prerequisites
- Linux, macOS, or Windows (with WSL2)
- At least 8 GB of RAM
- At least 5 GB of free disk space
- Internet connection for model download

## Installation

### Linux & macOS
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Verify installation
ollama --version
```

### Windows
1. Download Ollama for Windows from https://ollama.ai/download
2. Run the installer
3. Verify installation in PowerShell:
   ```powershell
   ollama --version
   ```

## Model Setup

### Option 1: Mistral 7B Instruct Q4_0 (Recommended)
This is the primary model used by the fleet dashboard API.

```bash
# Pull the quantized 4-bit instruct model
ollama pull mistral:7b-instruct-q4_0
```

**Specifications:**
- Model size: ~4.1 GB
- Memory required: ~6 GB RAM
- Quality: Excellent for instruction following
- Speed: Fast inference (~2-3 tokens/sec on CPU)

### Option 2: Mistral Latest (Fallback)
```bash
# Pull the latest Mistral model
ollama pull mistral:latest
```

**Specifications:**
- Model size: Variable (depends on version)
- Quality: Production-ready
- Speed: Fast

### Option 3: Generic Mistral (Second Fallback)
```bash
# Pull generic Mistral model
ollama pull mistral
```

## Starting Ollama Service

### Linux & macOS
Ollama typically starts automatically after installation. If not:

```bash
# Start Ollama service
ollama serve
```

The service will run on `http://localhost:11434` by default.

### Windows
Ollama runs as a background service automatically. Check status:

```powershell
# Test if Ollama is running
curl http://localhost:11434/api/version
```

## Verifying Setup

### 1. Check Service Status
```bash
# Test API endpoint
curl http://localhost:11434/api/version
```

Expected response:
```json
{"version":"0.1.x"}
```

### 2. List Available Models
```bash
ollama list
```

Expected output:
```
NAME                       ID              SIZE      MODIFIED
mistral:7b-instruct-q4_0   b17615239298    4.1 GB    2 hours ago
mistral:latest             6577803aa9a0    4.4 GB    2 hours ago
```

### 3. Test Model Generation
```bash
ollama run mistral:7b-instruct-q4_0 "Hello, how are you?"
```

### 4. Test with Fleet Dashboard API
Start the backend server and test:

```bash
# In terminal 1: Start backend
cd backend
python -m uvicorn main:app --reload

# In terminal 2: Test fleet insights
curl http://localhost:8000/api/fleet/insights | python -m json.tool
```

Check backend logs for:
```
✅ Generated fleet insights using model: mistral:7b-instruct-q4_0
```

## Configuration

### Backend Environment Variables
Update `backend/.env`:

```bash
# Default (local Ollama)
OLLAMA_API_URL=http://localhost:11434

# Remote Ollama instance
# OLLAMA_API_URL=http://your-server:11434
```

### Model Selection Priority
The system automatically tries models in this order:
1. `mistral:7b-instruct-q4_0` (if available)
2. `mistral:latest` (if available)
3. `mistral` (if available)
4. Rule-based feedback (always available)

## Troubleshooting

### Issue: Ollama service not responding
**Solution:**
```bash
# Check if service is running
curl http://localhost:11434/api/version

# If not running, start it
ollama serve
```

### Issue: Model not found
**Solution:**
```bash
# List installed models
ollama list

# Pull missing model
ollama pull mistral:7b-instruct-q4_0
```

### Issue: Out of memory
**Symptoms:** Slow responses, crashes, or timeouts

**Solutions:**
1. Use smaller quantized model:
   ```bash
   ollama pull mistral:7b-instruct-q3_k_m
   ```

2. Close other applications to free memory

3. Adjust model parameters (if needed):
   ```bash
   # Lower context window
   ollama run mistral:7b-instruct-q4_0 --ctx-size 2048
   ```

### Issue: Slow inference
**Solutions:**
1. Use GPU acceleration (if available):
   - Ensure CUDA/ROCm drivers installed
   - Ollama will automatically use GPU

2. Use smaller model:
   ```bash
   ollama pull mistral:7b-instruct-q4_0  # Already optimized
   ```

3. Reduce timeout in backend:
   - Edit `backend/services/ml_service.py`
   - Adjust `timeout=15` to lower value if needed

### Issue: Backend falls back to rule-based feedback
**Check:**
1. Is Ollama running?
   ```bash
   curl http://localhost:11434/api/version
   ```

2. Is model pulled?
   ```bash
   ollama list
   ```

3. Check backend logs for error messages

## Performance Optimization

### CPU Optimization
```bash
# Set number of threads
export OLLAMA_NUM_THREADS=4

# Start Ollama with optimization
ollama serve
```

### GPU Acceleration
Ollama automatically detects and uses:
- NVIDIA GPUs (via CUDA)
- AMD GPUs (via ROCm)
- Apple Silicon (via Metal)

No additional configuration needed!

### Memory Management
```bash
# Limit memory usage (in MB)
export OLLAMA_MAX_LOADED_MODELS=1
export OLLAMA_MAX_VRAM=4096

ollama serve
```

## Advanced Usage

### Running Multiple Models
```bash
# Keep multiple models loaded
export OLLAMA_MAX_LOADED_MODELS=2

# Now both models stay in memory
ollama pull mistral:7b-instruct-q4_0
ollama pull mistral:latest
```

### Custom Model Parameters
Modify `backend/services/ml_service.py` to customize:

```python
response = requests.post(
    f"{self.ollama_url}/api/generate",
    json={
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,  # Randomness (0-1)
            "top_k": 40,         # Diversity
            "top_p": 0.9,        # Nucleus sampling
            "num_predict": 150   # Max tokens
        }
    },
    timeout=15
)
```

### Remote Ollama Server
To use a remote Ollama instance:

1. Start Ollama on remote server:
   ```bash
   OLLAMA_HOST=0.0.0.0:11434 ollama serve
   ```

2. Update backend `.env`:
   ```bash
   OLLAMA_API_URL=http://remote-server:11434
   ```

## Testing AI Feedback

### Test Driver Feedback
```bash
curl -X POST http://localhost:8000/api/fleet/drivers/DRV001/feedback \
  | python -m json.tool
```

Look for AI-generated feedback like:
```json
{
  "feedback": "Outstanding performance with consistent high scores. Continue maintaining smooth driving patterns and anticipatory braking techniques."
}
```

### Test Fleet Insights
```bash
curl http://localhost:8000/api/fleet/insights \
  | python -m json.tool
```

### Monitor Backend Logs
Watch for model selection messages:
```
✅ Generated driver feedback using model: mistral:7b-instruct-q4_0
✅ Generated fleet insights using model: mistral:7b-instruct-q4_0
```

## Production Deployment

### Docker Setup
```dockerfile
# Dockerfile.ollama
FROM ollama/ollama:latest

# Pull model during build
RUN ollama serve & sleep 5 && \
    ollama pull mistral:7b-instruct-q4_0 && \
    pkill ollama

EXPOSE 11434
CMD ["ollama", "serve"]
```

### Docker Compose
```yaml
version: '3.8'

services:
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    command: serve
    
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - OLLAMA_API_URL=http://ollama:11434
    depends_on:
      - ollama

volumes:
  ollama_data:
```

### Health Checks
Add to backend health check:

```python
@app.get("/health")
async def health_check():
    # Check Ollama availability
    ollama_healthy = False
    try:
        response = requests.get(
            f"{os.getenv('OLLAMA_API_URL')}/api/version",
            timeout=2
        )
        ollama_healthy = response.status_code == 200
    except:
        pass
    
    return {
        "status": "healthy",
        "services": {
            "ml_service": ml_service is not None,
            "supabase": supabase_service.is_configured(),
            "ollama": ollama_healthy
        }
    }
```

## Resources

### Official Documentation
- Ollama: https://ollama.ai/
- Mistral AI: https://mistral.ai/

### Model Information
- Mistral 7B: https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.1
- Ollama Model Library: https://ollama.ai/library/mistral

### Community
- Ollama Discord: https://discord.gg/ollama
- GitHub Issues: https://github.com/ollama/ollama/issues

## Summary

To get AI feedback working:

1. **Install Ollama:**
   ```bash
   curl -fsSL https://ollama.ai/install.sh | sh
   ```

2. **Pull Mistral model:**
   ```bash
   ollama pull mistral:7b-instruct-q4_0
   ```

3. **Start Ollama service:**
   ```bash
   ollama serve
   ```

4. **Configure backend:**
   ```bash
   echo "OLLAMA_API_URL=http://localhost:11434" >> backend/.env
   ```

5. **Test:**
   ```bash
   curl -X POST http://localhost:8000/api/fleet/drivers/DRV001/feedback
   ```

That's it! The fleet dashboard will now use AI-powered feedback. If Ollama is unavailable, the system automatically falls back to rule-based feedback.
