require('dotenv').config();
const express = require('express');
const cors = require('cors');
const admin = require('firebase-admin');
const axios = require('axios');

const app = express();
app.use(cors());
app.use(express.json());

// Serve static HTML files from the root directory
const path = require('path');
const ADMIN_EMAIL = (process.env.TRUEPROFIT_ADMIN_EMAIL || 'hummuahmad@gmail.com').trim().toLowerCase();
const LEGACY_TRUEPROFIT_PATH = '/trueprofit_original.html';

// Never expose the legacy inline engine through the backend's static server.
app.use((req, res, next) => {
    if (req.path === LEGACY_TRUEPROFIT_PATH) {
        return res.status(404).send('Not found');
    }
    next();
});
app.use(express.static(path.join(__dirname, '..')));


// Initialize Firebase Admin (Requires Service Account credentials)
// The service account key should be provided via an environment variable or secret manager.
if (process.env.FIREBASE_SERVICE_ACCOUNT) {
    const serviceAccount = JSON.parse(process.env.FIREBASE_SERVICE_ACCOUNT);
    admin.initializeApp({
        credential: admin.credential.cert(serviceAccount)
    });
} else {
    console.warn("WARNING: FIREBASE_SERVICE_ACCOUNT not found. Admin SDK not initialized.");
}

const db = admin.apps.length ? admin.firestore(admin.app()) : null;

// The proprietary TRUEPROFIT application logic.
// This is kept securely on the server and only served to authorized users.
const TRUEPROFIT_ENGINE_CODE = `
console.log('TRUEPROFIT™ Engine Loaded Securely.');

const COSTS=["Purchase / stock / materials","Labour / your time","Transport","Packaging","Electricity / fuel / gas","Delivery / platform / transaction fees","Wastage / spoilage","Other direct costs"];

function fields(prefix){
    return COSTS.map(x=>'<div class="costline"><label>'+x+'</label><input data-'+prefix+' type="number" min="0" step="0.01" value="0"></div>').join("");
}

// Ensure the DOM elements exist before setting innerHTML
if (document.getElementById('qCosts')) document.getElementById('qCosts').innerHTML=fields("q");
if (document.getElementById('pCosts')) document.getElementById('pCosts').innerHTML=fields("p");

const money=n=>new Intl.NumberFormat("en-NG",{style:"currency",currency:"NGN",maximumFractionDigits:0}).format(Number(n)||0);
const num=id=>Math.max(0,Number(document.getElementById(id).value)||0);

const read=(k,f=[])=>{try{return JSON.parse(localStorage.getItem(k))??f}catch(e){return f}};
const write=(k,v)=>localStorage.setItem(k,JSON.stringify(v));
let current={unit:0,total:0,price:0,name:"Product",margin:.3};

window.show = function(id) {
    document.querySelectorAll(".screen").forEach(x=>x.classList.remove("active"));
    const el = document.getElementById(id);
    if(el) el.classList.add("active");
    document.querySelectorAll(".nav button").forEach(x=>x.classList.remove("active"));
    const nav = document.getElementById("nav-"+id);
    if(nav) nav.classList.add("active");
    
    if(id==="home") dashboard();
    if(id==="products") renderProducts();
    if(id==="sales") renderSales();
    if(id==="logsale") prepareSale();
    if(id==="analysis") renderAnalysis();
    window.scrollTo(0,0);
};

function totalCosts(prefix){
    return [...document.querySelectorAll("[data-"+prefix+"]")].reduce((a,x)=>a+Math.max(0,Number(x.value)||0),0);
}

window.runQuick = function(save) {
    const qty=Math.max(1,Math.floor(num("qQty"))),total=totalCosts("q"),unit=total/qty,margin=Math.min(.9,num("qMargin")/100);
    const name=document.getElementById('qProduct').value.trim()||"Product";
    const price=margin>=.9?unit:unit/(1-margin);
    current={unit,total,price,name,margin};
    
    document.getElementById('qrName').textContent=name+" · "+document.getElementById('bizType').value;
    document.getElementById('qrCost').textContent=money(unit);
    document.getElementById('qrTotal').textContent=money(total);
    document.getElementById('qrUnit').textContent=money(unit);
    document.getElementById('qrPrice').textContent=money(price);
    document.getElementById('qrProfit').textContent=money(price-unit);
    document.getElementById('qrExplain').textContent="Your entered costs total "+money(total)+" for "+qty+" unit(s), giving a real cost of "+money(unit)+" per unit. A "+Math.round(margin*100)+"% target margin gives a suggested price of "+money(price)+" per unit.";
    document.getElementById('dOriginal').value=Math.round(price);
    
    if(save){
        let p=read("tp_products");
        p.unshift({id:Date.now(),name,type:document.getElementById('bizType').value,cost:unit,price,margin});
        write("tp_products",p);
    }
    show("qresult");
};

window.saveProduct = function() {
    const name=document.getElementById('pName').value.trim();
    if(!name){alert("Please enter a name.");return;}
    const cost=totalCosts("p"),margin=Math.min(.9,num("pMargin")/100),price=margin>=.9?cost:cost/(1-margin);
    let p=read("tp_products");
    p.unshift({id:Date.now(),name,type:document.getElementById('pType').value,cost,price,margin});
    write("tp_products",p);
    show("products");
};

function esc(v){
    return String(v).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[c]));
}

window.renderProducts = function() {
    const p=read("tp_products"),el=document.getElementById('productList');
    if(!p.length){el.innerHTML='<div class="card empty">No saved products or services yet.</div>';return;}
    el.innerHTML=p.map(x=>'<div class="card"><div class="row"><div><h3>'+esc(x.name)+'</h3><div class="small muted">'+esc(x.type)+' · Cost '+money(x.cost)+' · Target '+money(x.price)+'</div></div><button class="danger" onclick="delProduct('+x.id+')">Delete</button></div></div>').join("");
};

window.delProduct = function(id) {
    write("tp_products",read("tp_products").filter(x=>x.id!==id));
    renderProducts();
};

window.openDiscountFromResult = function() {
    document.getElementById('dOriginal').value=Math.round(current.price);
    show("discount");
};

window.calcDiscount = function() {
    const original=num("dOriginal"),pct=Math.min(100,num("dPct")),sale=original*(1-pct/100),profit=sale-current.unit,margin=sale?profit/sale:0,ok=sale>=current.unit;
    const dOut = document.getElementById('dOut');
    dOut.classList.remove("hidden");
    dOut.innerHTML='<h2>Discount result</h2><div class="grid"><div class="result"><div class="label">NEW PRICE</div><div class="value">'+money(sale)+'</div></div><div class="result"><div class="label">PROFIT</div><div class="value">'+money(profit)+'</div></div><div class="result"><div class="label">MARGIN</div><div class="value">'+(margin*100).toFixed(1)+'%</div></div><div class="result"><div class="label">COST FLOOR</div><div class="value">'+money(current.unit)+'</div></div></div><p class="'+(ok?"good":"bad")+'">'+(ok?"✓ Still at or above your cost floor.":"⚠ Below your cost floor — this sale is losing money before other business expenses.")+'</p>';
};

window.prepareSale = function() {
    const p=read("tp_products");
    const sProduct = document.getElementById('sProduct');
    sProduct.innerHTML=p.length?p.map(x=>'<option value="'+x.id+'">'+esc(x.name)+'</option>').join(""):'<option value="">Create a product first</option>';
    document.getElementById('sDate').value=new Date().toISOString().slice(0,10);
    const fill=()=>{
        const x=p.find(y=>String(y.id)===sProduct.value);
        if(x){
            document.getElementById('sCost').value=Math.round(x.cost);
            document.getElementById('sPrice').value=Math.round(x.price);
        }
    };
    sProduct.onchange=fill;
    fill();
};

window.saveSale = function() {
    const p=read("tp_products");
    if(!p.length){alert("Save a product first.");show("products");return;}
    const name=document.getElementById('sProduct').selectedOptions[0]?.textContent||"Product",qty=Math.max(1,Math.floor(num("sQty"))),price=num("sPrice"),cost=num("sCost"),sale={id:Date.now(),date:document.getElementById('sDate').value,product:name,qty,price,cost,revenue:qty*price,totalCost:qty*cost,profit:qty*(price-cost)};
    sale.margin=sale.revenue?sale.profit/sale.revenue:0;
    let ss=read("tp_sales");
    ss.unshift(sale);
    write("tp_sales",ss);
    show("sales");
};

window.renderSales = function() {
    const ss=read("tp_sales"),rev=ss.reduce((a,s)=>a+s.revenue,0),prof=ss.reduce((a,s)=>a+s.profit,0);
    document.getElementById('sRevenue').textContent=money(rev);
    document.getElementById('sProfit').textContent=money(prof);
    document.getElementById('sMargin').textContent=(rev?prof/rev*100:0).toFixed(1)+"%";
    document.getElementById('sCount').textContent=ss.length;
    const salesList = document.getElementById('salesList');
    if(!ss.length){salesList.innerHTML='<div class="card empty">No sales recorded yet.</div>';return;}
    salesList.innerHTML='<div class="card"><div class="tablewrap"><table class="table"><tr><th>Date</th><th>Product</th><th>Qty</th><th>Revenue</th><th>Profit</th><th>Margin</th></tr>'+ss.map(s=>'<tr><td>'+esc(s.date)+'</td><td>'+esc(s.product)+'</td><td>'+s.qty+'</td><td>'+money(s.revenue)+'</td><td>'+money(s.profit)+'</td><td>'+(s.margin*100).toFixed(1)+'%</td></tr>').join("")+'</table></div></div>';
};

window.renderAnalysis = function() {
    const ss=read("tp_sales"),rev=ss.reduce((a,s)=>a+s.revenue,0),prof=ss.reduce((a,s)=>a+s.profit,0),by={};
    ss.forEach(s=>by[s.product]=(by[s.product]||0)+s.profit);
    let best="—";
    Object.keys(by).forEach(k=>{if(best==="—"||by[k]>by[best])best=k;});
    document.getElementById('aRevenue').textContent=money(rev);
    document.getElementById('aProfit').textContent=money(prof);
    document.getElementById('aMargin').textContent=(rev?prof/rev*100:0).toFixed(1)+"%";
    document.getElementById('aBest').textContent=best;
};

window.whatIf = function() {
    const cost=num("wCost"),inc=Number(document.getElementById('wIncrease').value)||0,price=num("wPrice"),newCost=cost*(1+inc/100),profit=price-newCost;
    const wOut = document.getElementById('wOut');
    wOut.classList.remove("hidden");
    wOut.innerHTML='<div class="grid"><div class="result"><div class="label">NEW COST</div><div class="value">'+money(newCost)+'</div></div><div class="result"><div class="label">NEW PROFIT</div><div class="value">'+money(profit)+'</div></div></div><p class="'+(profit>=0?"good":"bad")+'">'+(profit>=0?"Still profitable at the same selling price.":"The new cost would push the sale below cost.")+'</p>';
};

window.breakEven = function() {
    const fixed=num("bFixed"),contrib=num("bContribution");
    const bOut = document.getElementById('bOut');
    bOut.classList.remove("hidden");
    if(contrib<=0){bOut.innerHTML='<p class="bad">Contribution profit per unit must be greater than zero.</p>';return;}
    const units=Math.ceil(fixed/contrib);
    bOut.innerHTML='<div class="result"><div class="label">BREAK-EVEN UNITS</div><div class="value">'+units.toLocaleString("en-NG")+'</div></div>';
};

function dashboard(){
    const p=read("tp_products"),s=read("tp_sales");
    if(document.getElementById('dashProducts')) document.getElementById('dashProducts').textContent=p.length;
    if(document.getElementById('dashSales')) document.getElementById('dashSales').textContent=s.length;
    if(document.getElementById('dashRevenue')) document.getElementById('dashRevenue').textContent=money(s.reduce((a,x)=>a+x.revenue,0));
    if(document.getElementById('dashProfit')) document.getElementById('dashProfit').textContent=money(s.reduce((a,x)=>a+x.profit,0));
}

// Expose dashboard globally if needed, or call on init
dashboard();
`;

/**
 * 1. GET /api/engine.js
 * Protected endpoint. Returns the TRUEPROFIT engine code ONLY if the user is authenticated 
 * AND has a valid entitlement in Firestore.
 */
app.get('/api/engine.js', async (req, res) => {
    try {
        const authHeader = req.headers.authorization;
        if (!authHeader || !authHeader.startsWith('Bearer ')) {
            return res.status(401).send('/* Unauthorized: Missing or invalid token */');
        }

        const idToken = authHeader.split('Bearer ')[1];
        
        if (!db) {
            console.error('TRUEPROFIT authorization unavailable: Firebase Admin/Firestore is not configured.');
            return res.status(503).send('/* Service unavailable: authorization is not configured. */');
        }

        // Verify the Firebase ID token
        const decodedToken = await admin.auth().verifyIdToken(idToken);
        const email = decodedToken.email;
        
        if (!email || decodedToken.email_verified !== true) {
            return res.status(403).send('/* Forbidden: User has no email */');
        }

        // Verify Entitlement in Firestore
        if (email.toLowerCase() !== ADMIN_EMAIL) {
            if (!db) return res.status(500).send('/* Server Error: Database not configured. */');
            const entitlementRef = db.collection('entitlements').doc(email);
            const docSnap = await entitlementRef.get();
            if (!docSnap.exists) {
                return res.status(403).send('/* Forbidden: No TRUEPROFIT entitlement found for this account. */');
            }
            const data = docSnap.data();
            const isActive = data.active === true || String(data.active).toLowerCase().trim() === 'true';
            if (!isActive) {
                return res.status(403).send('/* Forbidden: Your TRUEPROFIT entitlement is inactive. */');
            }
        }

        // Access Granted. Return the actual JavaScript engine.
        res.setHeader('Content-Type', 'application/javascript');
        res.send(TRUEPROFIT_ENGINE_CODE);

    } catch (error) {
        console.error('Authentication or Server Error:', error);
        res.status(500).send('/* Server Error */');
    }
});

/**
 * 2. POST /webhooks/selar
 * Webhook endpoint for Selar to notify us of successful purchases.
 */
app.post('/webhooks/selar', async (req, res) => {
    try {
        // According to Selar documentation, they post the transaction data here.
        // It's recommended to verify the transaction using the Selar API to prevent spoofing.
        const webhookData = req.body;
        
        // Ensure this is a successful transaction
        const reference = webhookData.reference;
        if (!reference) {
            return res.status(400).send('Missing reference');
        }

        // 1. VERIFY WITH SELAR API (Requires SELAR_BEARER_TOKEN environment variable)
        const selarToken = process.env.SELAR_BEARER_TOKEN;
        if (!selarToken) {
            console.error("Missing SELAR_BEARER_TOKEN to verify purchase.");
            return res.status(500).send('Server configuration missing');
        }

        // Make a GET request to Selar API to verify the transaction reference
        const selarResponse = await axios.get(`https://selar.co/api/v1/transactions/${reference}`, {
            headers: {
                'Authorization': `Bearer ${selarToken}`
            }
        });

        const transaction = selarResponse.data;
        
        if (transaction.status !== 'success') {
            console.warn(`Transaction ${reference} is not successful.`);
            return res.status(400).send('Transaction not successful');
        }

        // 2. CHECK PRODUCT MATCH
        const expectedProductId = String(process.env.SELAR_TRUEPROFIT_PRODUCT_ID || '').trim();
        if (!expectedProductId) {
            console.error("Missing SELAR_TRUEPROFIT_PRODUCT_ID.");
            return res.status(503).send('Product verification is not configured');
        }
        const productIds = [
            transaction.product_id,
            transaction.productId,
            transaction.product?.id,
            transaction.product?.product_id,
            transaction.product?.productId,
            transaction.product?.code,
            transaction.data?.product_id,
            transaction.data?.productId,
            transaction.data?.product?.id,
            transaction.data?.product?.product_id,
            transaction.data?.product?.code,
        ].filter(value => value !== undefined && value !== null)
            .map(value => String(value).trim());
        if (!productIds.includes(expectedProductId)) {
            console.warn(`Transaction ${reference} is for an unapproved product.`);
            return res.status(403).send('Transaction product is not TRUEPROFIT');
        }

        const customerEmail = String(transaction.customer?.email || '').trim().toLowerCase();
        if (!customerEmail) {
            return res.status(400).send('Missing customer email');
        }

        // 3. CREATE/UPDATE ENTITLEMENT IN FIRESTORE
        if (!db) {
            console.error("Database not initialized, cannot save entitlement.");
            return res.status(503).send('Authorization database is not configured');
        }
        const entitlementRef = db.collection('entitlements').doc(customerEmail);
        await entitlementRef.set({
            email: customerEmail,
            active: true,
            orderId: reference,
            purchaseDate: admin.firestore.FieldValue.serverTimestamp(),
            product: 'TRUEPROFIT',
        }, { merge: true }); // Idempotent update
        
        console.log(`Entitlement granted to ${customerEmail} for transaction ${reference}`);

        res.status(200).send('Webhook processed successfully');
    } catch (error) {
        console.error('Webhook Error:', error.message);
        res.status(500).send('Webhook processing failed');
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Secure TRUEPROFIT Backend running on port ${PORT}`);
});
