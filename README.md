# Aero-Sense: Intelligent Engine Health & MLOps Platform

Aero-Sense is a predictive maintenance platform for aircraft engines, combining NASA jet engine simulation data with live weather data to calculate Remaining Useful Life (RUL) in real-time. Built with Google Cloud Native technologies, our polyglot microservices architecture uses Go for high-performance ingestion, Python with Vertex AI for AI modeling, and Next.js for an interactive dashboard. 

Key Features:
- **Predictive Maintenance:** RUL estimation using XGBoost and Vertex AI
- **Hybrid Data Streams:** Sensor + live weather data via Confluent Kafka
- **GenAI Support:** Gemini 1.5 Pro generates maintenance prescriptions
- **Full Observability:** Metrics, model drift, and API latency monitored via Datadog
- **Cloud Native & Polyglot:** Cloud Run, Memorystore, BigQuery, Firestore

This project was developed for the Google Cloud Partner Catalyst Hackathon, addressing the Datadog and Confluent challenges. 

**Repo includes:** source code, deployment instructions, and Datadog configuration JSONs. Demo video and traffic generator script included for testing.
