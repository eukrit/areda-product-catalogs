import { initializeApp, cert, getApps, App } from "firebase-admin/app";
import { getFirestore } from "firebase-admin/firestore";

let adminApp: App;

if (getApps().length === 0) {
  if (process.env.GOOGLE_APPLICATION_CREDENTIALS) {
    adminApp = initializeApp({
      credential: cert(process.env.GOOGLE_APPLICATION_CREDENTIALS),
      projectId: "ai-agents-go",
    });
  } else {
    // On Cloud Run, uses default service account
    adminApp = initializeApp({ projectId: "ai-agents-go" });
  }
} else {
  adminApp = getApps()[0];
}

// Connect to the areda-product-catalogs database (separate from default)
const adminDb = getFirestore(adminApp, "areda-product-catalogs");

export { adminApp, adminDb };
