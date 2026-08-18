# GhIE E-Card Generation Service

A **FastAPI microservice** responsible for generating personalized GhIE Student E-Cards from student information and passport photos.

## Features

* Dynamic E-Card generation
* Passport photo processing with **Pillow**
* QR-code generation and embedding
* Student information rendering
* In-memory image processing using **`BytesIO`**
* REST API communication with the Spring Boot backend
* Dockerized deployment

## Architecture

```text
Spring Boot Backend
        │
        │ REST Request
        │ Student data + image
        ▼
   FastAPI Service
        │
        ├── Image Processing
        ├── Card Rendering
        └── QR Generation
        │
        ▼
  Binary E-Card Image
        │
        ▼
BREVO email automation / delivery to client email address
Spring Boot Backend-> Marks Student as email_sent in DB
```

## Image Processing

Images are processed in memory using Python's `BytesIO`, avoiding unnecessary temporary files.



## Tech Stack

* Python 3.11
* FastAPI
* Pillow
* OpenCV
* QR Code
* Docker
* REST API

## Status

✅ E-Card generation
✅ Image processing
✅ QR verification
✅ Spring Boot integration
✅ Docker deployment
🚧 Face ID validation — **Under Development**
