# TRUEPROFIT Backend Integration

This directory contains the secure backend architecture for the TRUEPROFIT application.

## Overview

The TRUEPROFIT application is protected by a secure, server-side entitlement check. The architecture operates as follows:

1. **Selar Purchase (Webhook):** When a user successfully purchases TRUEPROFIT via Selar, Selar sends a POST request to this backend (`/webhooks/selar`). 
2. **Transaction Verification:** The backend makes a secure API request to Selar to independently verify the transaction using your `SELAR_BEARER_TOKEN`. This prevents webhook spoofing.
3. **Entitlement Creation:** Upon successful verification, an entitlement record is created in Firebase Firestore (`entitlements/{customerEmail}`).
4. **Application Access:** The frontend application (static HTML) does **not** contain the core TRUEPROFIT logic. Instead, when a user logs in via Firebase Authentication, the frontend requests the core JavaScript engine from the backend (`/api/engine.js`).
5. **Authorization:** The backend verifies the user's Firebase token and checks Firestore for a valid entitlement. If valid, the proprietary JavaScript engine is returned and executed. Otherwise, access is denied.

## Required Credentials / Configuration

To deploy this backend, you must configure the following environment variables (e.g., in a `.env` file or your hosting provider's secret manager):

### 1. Firebase Admin SDK
- `FIREBASE_SERVICE_ACCOUNT`: A JSON string containing your Firebase Service Account credentials. You can generate this in the Firebase Console under **Project Settings > Service Accounts > Generate new private key**.
  
### 2. Selar API Integration
- `SELAR_BEARER_TOKEN`: Your Selar developer integration token. You can activate and find this in your Selar Supplier Settings under the API integration section. This is required for transaction verification.
- `SELAR_TRUEPROFIT_PRODUCT_ID`: The internal ID of your TRUEPROFIT product on Selar (e.g. from the URL `https://selar.com/28o4b14m9g`, the code or specific product ID) to ensure the webhook is for the correct product.

## Deployment Options

This backend is designed as an Express.js server, but it can be easily adapted. Recommended deployment methods:

1. **Firebase Cloud Functions (Recommended):** Convert the Express app to a Firebase HTTP function. This is seamless since you are already using Firebase Firestore.
2. **Google Cloud Run / Heroku / Render:** Deploy the Node.js server using a Dockerfile or standard Node.js deployment.

## Existing Website Compatibility

The static website (built via `build.py`) remains entirely intact and functional. The TRUEPROFIT application HTML (`trueprofit-app.html`) will have a modified authentication flow that integrates with this backend API, ensuring that only authorized users receive the functional logic.
