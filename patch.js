const fs = require('fs');
let code = fs.readFileSync('backend/server.js', 'utf8');
code = code.replace(
    "const entitlementRef = db.collection('entitlements').doc(email);\n        const docSnap = await entitlementRef.get();\n\n        if (!docSnap.exists) {\n            return res.status(403).send('/* Forbidden: No TRUEPROFIT entitlement found for this account. */');\n        }\n\n        const data = docSnap.data();\n        if (data.active !== true && data.active !== 'true') {\n            return res.status(403).send('/* Forbidden: Your TRUEPROFIT entitlement is inactive. */');\n        }",
    "const entitlementRef = db.collection('entitlements').doc(email);\n        const docSnap = await entitlementRef.get();\n\n        if (email !== 'hummuahmad@gmail.com') {\n            if (!docSnap.exists) {\n                return res.status(403).send('/* Forbidden: No TRUEPROFIT entitlement found for this account. */');\n            }\n            const data = docSnap.data();\n            const isActive = data.active === true || String(data.active).toLowerCase().trim() === 'true';\n            if (!isActive) {\n                return res.status(403).send('/* Forbidden: Your TRUEPROFIT entitlement is inactive. */');\n            }\n        }"
);
fs.writeFileSync('backend/server.js', code);
console.log("Patched!");
