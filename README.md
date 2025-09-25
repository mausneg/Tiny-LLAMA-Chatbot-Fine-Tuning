# Tiny-LLAMA-Chatbot-Fine-Tuning

A conversational AI chatbot powered by TinyLlama-1.1B model with fine-tuning capabilities. This project provides a FastAPI-based REST API for chat interactions with conversation memory and Docker deployment support.

## Features

- 🤖 **TinyLlama-1.1B Model**: Lightweight yet powerful language model
- 💬 **Conversation Memory**: Maintains chat history with intelligent prompt management
- 🚀 **FastAPI Backend**: High-performance REST API with automatic documentation
- 🐳 **Docker Support**: Easy deployment with Docker Compose
- 🔧 **Fine-tuning Ready**: Built with PEFT (Parameter Efficient Fine-Tuning) support
- ⚡ **Optimized Performance**: 8-bit quantization and GPU acceleration
- 🌐 **CORS Enabled**: Ready for web frontend integration

## Architecture

```
├── api/                    # FastAPI application
│   ├── app.py             # Main API server
│   ├── Dockerfile         # API container config
│   └── requirements.txt   # Python dependencies
├── app/                   # Alternative app structure
├── components/            # Training and deployment components
│   ├── trainer.py         # Model training utilities
│   └── pusher.py          # Model deployment utilities
├── utils/                 # Utility modules
│   ├── data_model.py      # Pydantic models
│   └── io.py              # I/O operations
├── saved_models/          # Fine-tuned model storage
├── nginx/                 # Reverse proxy configuration
└── docker-compose.yml     # Multi-container orchestration
```

## Quick Start

### Prerequisites

- Docker and Docker Compose
- NVIDIA GPU (optional, for faster inference)
- CUDA toolkit (if using GPU)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/Tiny-LLAMA-Chatbot-Fine-Tuning.git
   cd Tiny-LLAMA-Chatbot-Fine-Tuning
   ```

2. **Start the application**
   ```bash
   docker compose up --build
   ```

3. **Access the API**
   - API Documentation: http://localhost:8082/docs
   - API Base URL: http://localhost:8082/api/v1/

### GPU Support (Recommended)

For GPU acceleration, modify `docker-compose.yml`:

```yaml
services:
  app:
    build:
      context: .
      dockerfile: api/Dockerfile
    ports:
      - "5003:5003"
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
```

## API Endpoints

### POST `/api/v1/conversation`
Start or continue a conversation with the chatbot.

**Request Body:**
```json
{
  "role": "user",
  "content": ["Your message here"]
}
```

**Response:**
```json
{
  "response": "Assistant's response"
}
```

### DELETE `/api/v1/conversation`
Clear conversation history.

**Response:**
```json
{
  "message": "Conversation cleared",
  "status": "success"
}
```

## Configuration

### Model Settings
- **Model**: TinyLlama-1.1B-Chat-v1.2
- **Max Token Length**: 2048 tokens
- **Quantization**: 8-bit for memory efficiency
- **Device**: Auto-detection (GPU preferred)

### Performance Tuning
Modify these parameters in `api/app.py`:
```python
MAX_LENGTH = 2048          # Maximum prompt length
max_new_tokens = 100       # Limit response length
temperature = 0.7          # Response creativity
```

## Development

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the API server
cd api
uvicorn app:app --host 0.0.0.0 --port 5003 --reload
```

### Model Fine-tuning
The project supports fine-tuning with PEFT. Training notebooks and utilities are available in:
- `saved_models/Tiny_LLAMA_1_1B_Instruction_Tuning.ipynb`
- `components/trainer.py`

## Deployment

### Production Deployment
Use the production Docker Compose configuration:
```bash
docker compose -f docker-compose.prod.yml up -d
```

### Environment Variables
```bash
MODEL_NAME=TinyLlama-1.1B-Chat-v1.2
MAX_LENGTH=2048
CUDA_VISIBLE_DEVICES=0  # GPU device ID
```

## Troubleshooting

### Common Issues

1. **Slow Response Times**
   - Ensure GPU is available and configured
   - Reduce `max_new_tokens` parameter
   - Check system resources

2. **Memory Issues**
   - Enable 8-bit quantization (already enabled)
   - Reduce `MAX_LENGTH` parameter
   - Use smaller batch sizes

3. **Timeout Errors**
   - Increase Nginx timeout settings
   - Optimize model parameters
   - Check Docker resource limits

### Performance Monitoring
```bash
# Monitor GPU usage
nvidia-smi

# Check container logs
docker compose logs -f app

# Monitor system resources
docker stats
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [TinyLlama](https://github.com/jzhang38/TinyLlama) - Base language model
- [Hugging Face Transformers](https://huggingface.co/transformers/) - Model implementation
- [PEFT](https://github.com/huggingface/peft) - Parameter-efficient fine-tuning
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework

## Support

For questions and support:
- Open an issue on GitHub
- Check the [API documentation](http://localhost:8082/docs)
- Review the troubleshooting section above

---

**Note**: This chatbot is designed for educational and research purposes. Please ensure responsible AI usage and consider implementing appropriate safety measures for production deployments.