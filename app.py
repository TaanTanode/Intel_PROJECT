import streamlit as st
import joblib
import pandas as pd
import numpy as np

# โหลดโมเดล
stock_model = joblib.load('stock_model.pkl')  # โมเดล Random Forest
svm_model = joblib.load('svm_tesla_model.pkl')  # โมเดล SVM
scaler = joblib.load("scaler.pkl")
diabetes_model = joblib.load('diabetes_model.pkl')  # โมเดลเบาหวาน

# ฟังก์ชันทำนายราคาหุ้นด้วย Random Forest
def predict_stock_rf(open_price, high_price, low_price, volume):
    input_data = pd.DataFrame([[open_price, high_price, low_price, volume]], columns=["Open", "High", "Low", "Volume"])
    prediction = stock_model.predict(input_data)
    return prediction[0]

# ฟังก์ชันทำนายราคาหุ้นด้วย SVM
def predict_stock_svm(open_price, high_price, low_price, volume):
    input_data = pd.DataFrame([[open_price, high_price, low_price, volume]], columns=scaler.feature_names_in_)  # ✅ แก้ไขตรงนี้
    input_data_scaled = scaler.transform(input_data)
    prediction = svm_model.predict(input_data_scaled)
    return prediction[0]

# ฟังก์ชันทำนายโรคเบาหวาน
def predict_diabetes(pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age):
    input_data = pd.DataFrame([[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age]],
                              columns=["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"])
    prediction = diabetes_model.predict(input_data)
    return prediction[0]

# เมนูเลือกหน้า
page = st.sidebar.radio("MENU:", ["Home", "Machine Learning Model", "Neural Network Model", "ML Description", "NN Description"])

if page == "Home":
    st.title("Welcome to Our Website")
    st.write("""
เว็บไซต์นี้ให้บริการ **การพยากรณ์หุ้น** และ **การทำนายความเสี่ยงโรคเบาหวาน** ด้วยโมเดล Machine Learning  
คุณสามารถเลือกใช้โมเดลที่เหมาะสมและดูผลการพยากรณ์ได้อย่างง่ายดาย


### Features
1. **พยากรณ์ราคาหุ้น Tesla**  
   - ใช้โมเดล Machine Learning ได้แก่ **Linear Regression, Support Vector Regression (SVR)** 
   - ป้อนค่าปัจจัยที่เกี่ยวข้อง เช่น ราคาเปิด ราคาสูงสุด ราคาต่ำสุด และปริมาณการซื้อขาย  
   - เปรียบเทียบผลลัพธ์จากโมเดลต่างๆ เพื่อเลือกแนวทางที่ดีที่สุด

2. **ทำนายความเสี่ยงโรคเบาหวาน**  
   - ใช้ **Artificial Neural Network (MLP)** ในการวิเคราะห์ข้อมูล  
   - ป้อนค่าตัวแปรสุขภาพ เช่น ระดับน้ำตาลในเลือด ความดันโลหิต และดัชนีมวลกาย  
   - ระบบจะแสดงผลว่า **มีความเสี่ยง (⚠️) หรือไม่มีความเสี่ยง (😊)**  

### How to Use
1. **เลือกเมนู "Machine Learning Model"** เพื่อพยากรณ์ราคาหุ้น **หรือ**
2. **เลือกเมนู "Neural Network Model"** เพื่อตรวจสอบความเสี่ยงโรคเบาหวาน  
3. ป้อนค่าข้อมูลที่ต้องการวิเคราะห์ แล้วกด **พยากรณ์**  
4. ระบบจะแสดงผลการทำนาย พร้อมรายงานผลลัพธ์
             

""")
    


    st.header("✨ **ใช้ Machine Learning เพื่อช่วยในการตัดสินใจอย่างชาญฉลาดได้แล้ววันนี้!** ✨")
elif page == "Machine Learning Model":
    st.title("TESLA Stock Price Prediction")
    
    open_price = st.number_input("ราคาปิดของวันก่อนหน้า:", min_value=0.0, format="%.2f")
    high_price = st.number_input("ราคาสูงสุดของวันก่อนหน้า:", min_value=0.0, format="%.2f")
    low_price = st.number_input("ราคาต่ำสุดของวันก่อนหน้า:", min_value=0.0, format="%.2f")
    volume = st.number_input("ปริมาณการซื้อขาย (Volume):", min_value=0)
    
    model_choice = st.radio("เลือกโมเดลทำนายราคาหุ้น:", ["Random Forest", "SVM"])
    
    if st.button("Predict"):
        if model_choice == "Random Forest":
            prediction = predict_stock_rf(open_price, high_price, low_price, volume)
        else:
            prediction = predict_stock_svm(open_price, high_price, low_price, volume)
        
        st.write(f"ทำนายราคาหุ้นวันถัดไป: {prediction:.2f}")

elif page == "Neural Network Model":
    st.title("Diabetes Prediction")
    
    pregnancies = st.number_input("จำนวนการตั้งครรภ์:", min_value=0)
    glucose = st.number_input("ระดับน้ำตาลในเลือด:", min_value=0)
    blood_pressure = st.number_input("ความดันโลหิต:", min_value=0)
    skin_thickness = st.number_input("ความหนาของผิวหนัง (Skin Thickness):", min_value=0)
    insulin = st.number_input("ระดับอินซูลิน (Insulin):", min_value=0)
    bmi = st.number_input("ค่าดัชนีมวลกาย (BMI):", min_value=0.0, format="%.2f")
    dpf = st.number_input("ค่าความเสี่ยงทางพันธุกรรม (Diabetes Pedigree Function):", min_value=0.0, format="%.3f")
    age = st.number_input("อายุ:", min_value=0)
    
    if st.button("Predict"):
        if all(val >= 0 for val in [pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age]):
            prediction = predict_diabetes(pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age)
            if prediction == 1:
                st.toast("⚠️ เสี่ยง ⚠️", icon="⚠️")
            else:
                st.toast("😊 ไม่เสี่ยง 😊", icon="✅")
        else:
            st.write("กรุณากรอกข้อมูลทั้งหมด")

elif page == "ML Description":
    st.title("**การพยากรณ์ราคาหุ้นด้วย Machine Learning:** การสร้างโมเดลด้วย Linear Regression and SVR")
    st.write("")
    st.image("https://designindc.com/wp-content/uploads/2022/12/Machine-Learning-768x432.jpg", caption="ขอขอบคุณรูปภาพจาก https://designindc.com")
    
    st.write("""&nbsp;&nbsp;&nbsp;&nbsp;การพยากรณ์ราคาหุ้นเป็นหนึ่งในหัวข้อที่ได้รับความสนใจมากที่สุดในแวดวงการเงินและปัญญาประดิษฐ์ เนื่องจากราคาหุ้นได้รับอิทธิพล
             จากปัจจัยหลายประการ เช่น ภาวะเศรษฐกิจ นโยบายของรัฐบาล แนวโน้มตลาด และความเชื่อมั่นของนักลงทุน การใช้ Machine Learning 
             ช่วยให้เราสามารถวิเคราะห์แนวโน้มของตลาดหุ้นและสร้างโมเดลที่สามารถพยากรณ์ราคาหุ้นได้อย่างแม่นยำมากขึ้นในบทความนี้ เราจะพัฒนาโมเดล
             พยากรณ์ราคาหุ้นโดยใช้ Linear Regression และ SVR ซึ่งเป็นอัลกอริธึมที่มีประสิทธิภาพสูงสำหรับปัญหาการพยากรณ์เชิงตัวเลข (Regression) 
             เราจะอธิบายทฤษฎีที่เกี่ยวข้อง กระบวนการเตรียมข้อมูล และการนำโมเดลไปใช้จริงในแอปพลิเคชัน
        ในหน้านี้ คุณสามารถทำนายราคาหุ้นสำหรับวันถัดไป โดยการกรอกข้อมูลต่างๆ เช่น ราคาปิดของวันก่อนหน้า ราคาสูงสุดและต่ำสุด รวมถึงปริมาณการซื้อขาย
        โดยโมเดลของเราจะใช้ข้อมูลเหล่านี้ในการทำนายราคาหุ้นในวันถัดไป
    """)
    st.header("ทฤษฎีเบื้องหลังการพยากรณ์ราคาหุ้น")
    st.write("&nbsp;&nbsp;&nbsp;&nbsp;ก่อนที่เราจะเข้าสู่การสร้างโมเดล เราต้องเข้าใจก่อนว่าเหตุใดการพยากรณ์ราคาหุ้นจึงเป็นงานที่ท้าทาย และแนวคิดเบื้องต้นของอัลกอริธึมที่เราจะใช้")
    st.write("""&nbsp;&nbsp;&nbsp;&nbsp;**ทำไมการพยากรณ์ราคาหุ้นถึงยาก**
    ราคาหุ้นมีลักษณะเป็น Time Series Data หรือข้อมูลที่เปลี่ยนแปลงตามเวลา ซึ่งแตกต่างจากข้อมูลทั่วไปที่ไม่มีลำดับของเวลาเข้ามาเกี่ยวข้อง
    ความท้าทายหลักในการพยากรณ์ราคาหุ้น ได้แก่""")
    st.write("")
    st.write("""
      1. ความผันผวนสูง: ราคาหุ้นเปลี่ยนแปลงตลอดเวลาและได้รับผลกระทบจากปัจจัยที่ไม่สามารถคาดการณ์ได้ เช่น ข่าวสาร หรือเหตุการณ์ทางเศรษฐกิจ
      2. ปัจจัยที่ส่งผลมีจำนวนมาก: นอกเหนือจากข้อมูลทางเทคนิค เช่น ราคาเปิด ปิด สูงสุด ต่ำสุด และปริมาณการซื้อขายแล้ว ราคาหุ้นยังได้รับอิทธิพลจากปัจจัยอื่นๆ เช่น นโยบายของธนาคารกลาง รายงานผลประกอบการ และแนวโน้มตลาดโลก
      3. Overfitting และ Underfitting: หากโมเดลมีความซับซ้อนเกินไป อาจเกิด Overfitting (เรียนรู้ข้อมูลฝึกมากเกินไปจนใช้งานกับข้อมูลใหม่ไม่ได้) แต่ถ้าโมเดลง่ายเกินไป อาจเกิด Underfitting (โมเดลไม่สามารถจับแนวโน้มที่แท้จริงของข้อมูลได้)
    """)
    
    st.write("")
    st.header("Linear Regression")
    st.subheader("แนวคิดพื้นฐานของ Linear Regression")
    st.write("""&nbsp;&nbsp;&nbsp;&nbsp;Linear Regression (การถดถอยเชิงเส้น) เป็นอัลกอริธึม Machine Learning ที่ใช้สำหรับการพยากรณ์ค่าตัวเลขโดยพยายามหา เส้นตรงที่ดีที่สุด ซึ่งสามารถใช้ในการคาดการณ์ค่าของตัวแปรเป้าหมาย (Dependent Variable,
y) จากค่าของตัวแปรอิสระ (Independent Variables,X)
Linear Regression เป็นอัลกอริธึมที่เข้าใจง่ายและใช้งานได้อย่างแพร่หลาย โดยเฉพาะในปัญหาที่ข้อมูลมีความสัมพันธ์เชิงเส้น กล่าวคือ ถ้าหากเราวาดกราฟระหว่างตัวแปรอิสระกับตัวแปรเป้าหมายแล้วพบว่ามีแนวโน้มเป็นเส้นตรง Linear Regression จะสามารถใช้งานได้ดี
""")
    
    st.subheader("สมการของ Linear Regression")
    st.code("""y=w0+w1X1+w2X2+...+wnXn+ϵ""")
    st.write("")

    st.subheader("การหาค่า w₀ และ w₁ (Least Squares Method)")
    st.write("""&nbsp;&nbsp;&nbsp;&nbsp;Linear Regression ใช้วิธี Least Squares Method ในการหาค่า w0 และ w1 โดยพยายามทำให้ ผลรวมของค่าคลาดเคลื่อน (Error) ยกกำลังสองมีค่าน้อยที่สุด

ค่าคลาดเคลื่อน (Residual) คือความแตกต่างระหว่างค่าจริง และค่าที่โมเดลพยากรณ์""")
    st.write("เราหาค่าสัมประสิทธิ์ w0 และ w1 โดยพยายามลดค่าของ Mean Squared Error (MSE) ซึ่งมีสมการดังนี้")

    st.write("")
    st.subheader("การประเมินผลของ Linear Regression")
    st.write("เมื่อเราสร้างโมเดลเสร็จแล้ว เราต้องประเมินผลว่าโมเดลมีประสิทธิภาพมากเพียงใด วิธีการวัดผลที่นิยมใช้ ได้แก่")
    st.write("1. Mean Squared Error (MSE): วัดความคลาดเคลื่อนโดยหาค่าเฉลี่ยของความผิดพลาดยกกำลังสอง")
    st.write("""2. R-squared : ใช้วัดว่าโมเดลสามารถอธิบายความแปรปรวนของข้อมูลได้ดีเพียงใด มีค่าอยู่ระหว่าง 0 ถึง 1 ถ้าค่า 
  ใกล้ 1 แสดงว่าโมเดลสามารถอธิบายความแปรปรวนของข้อมูลได้ดี""")
    st.write("ถ้าค่าใกล้ 0 หมายความว่าโมเดลยังไม่สามารถอธิบายข้อมูลได้ดี")
    st.write("")

    st.subheader("จุดแข็งและข้อจำกัดของ Linear Regression")
    st.write("ข้อดี")
    st.write("""
      1.  เป็นโมเดลที่เข้าใจง่ายและอธิบายได้ชัดเจน
      2.  สามารถใช้เป็นพื้นฐานสำหรับอัลกอริธึมที่ซับซ้อนกว่า
      3.  ทำงานได้ดีถ้าข้อมูลมีความสัมพันธ์เชิงเส้น""")
    st.write("แต่ก็มีข้อเสียเช่นเดียวกัน")
    st.write("""
    1.  ใช้ไม่ได้ดีถ้าข้อมูลไม่มีความสัมพันธ์เชิงเส้น
    2.  อ่อนไหวต่อ Outliers มาก
    3.  ไม่สามารถจับความสัมพันธ์ที่ซับซ้อนได้

""")
    st.write("")
    st.subheader("การนำ Linear Regression ไปใช้พยากรณ์ราคาหุ้น Tesla")
    st.write(""" 
    &nbsp;&nbsp;&nbsp;&nbsp;Linear Regression เป็นอัลกอริธึมที่นิยมใช้ในการวิเคราะห์ข้อมูลทางการเงิน เช่น การทำนายราคาหุ้น โดยใช้ข้อมูลในอดีต เช่น ราคาหุ้นเปิด (Open),  ราคาสูงสุด (High),  ราคาต่ำสุด (Low)และ
ปริมาณการซื้อขาย (Volume) เพื่อพยากรณ์ราคาปิดของหุ้น (Close Price)
""")
    st.write("")

    st.subheader("การพัฒนาโมเดล Linear Regression อย่างละเอียดทีละขั้นตอน")
    st.write("""1. โหลดไลบรารีที่จำเป็น
ก่อนที่เราจะสร้างโมเดล Machine Learning เราต้องโหลดไลบรารีที่จำเป็น เช่น numpy, pandas, matplotlib และ sklearn""")
    st.code("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score""")
    st.write("""
    -  numpy และ pandas ใช้สำหรับจัดการข้อมูลเชิงตัวเลขและตาราง
    -  matplotlib.pyplot ใช้สำหรับวาดกราฟช่วยในการวิเคราะห์ข้อมูล
    -  train_test_split ใช้แบ่งข้อมูลออกเป็นชุด Train และ Test
    -  LinearRegression คือโมเดล Linear Regression ที่เราจะใช้
    -  mean_squared_error และ r2_score ใช้วัดความแม่นยำของโมเดล
    """)
    
    st.write("2. โหลดข้อมูลและดูโครงสร้างของข้อมูล")
    st.code("""df = pd.read_csv("tesla_stock_data.csv")
df.head()
""")
    st.write("""pd.read_csv("tesla_stock_data.csv") โหลดข้อมูลราคาหุ้น Tesla จากไฟล์ CSV ส่วน df.head() แสดงตัวอย่าง 5 แถวแรกของข้อมูล""")
    st.write("3. เลือก Feature และ Target")
    st.code("""
    X = df[['Open', 'High', 'Low', 'Volume']]
y = df['Close']
""")
    st.write("X คือ Feature Matrix ซึ่งเป็นตัวแปรอิสระ (Open, High, Low, Volume)และ y คือ Target Variable หรือค่าที่ต้องการพยากรณ์ (Close)")
    st.write("4. แบ่งข้อมูลเป็นชุด Train และ Test")
    st.code("""X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
""")
    st.write("""train_test_split() แบ่งข้อมูลเป็น 80% Train และ 20% Test
random_state=42 ใช้กำหนดค่า seed ให้ได้ผลลัพธ์เดิมทุกครั้ง""")
    st.write("5. สร้างโมเดล Linear Regression และฝึกโมเดล")
    st.code("""model = LinearRegression()
model.fit(X_train, y_train)
""")
    st.write("""&nbsp;&nbsp;&nbsp;&nbsp;LinearRegression() สร้างอ็อบเจ็กต์โมเดล fit(X_train, y_train) ฝึกโมเดลโดยหาค่าค่าสัมประสิทธิ์ โมเดลใช้ Ordinary Least Squares (OLS) เพื่อลดค่าความคลาดเคลื่อน
OLS หาค่าที่ทำให้ ผลรวมของค่าคลาดเคลื่อนยกกำลังสองน้อยที่สุด""")
    st.write("6. ดูค่าสัมประสิทธิ์ของโมเดล")
    st.code("""print("Intercept:", model.intercept_)
print("Coefficients:", model.coef_)
""")
    st.write("ตัวอย่างผลลัพธ์ที่ได้")
    st.code("""Intercept: 2.5
Coefficients: [0.8, 0.6, 0.7, -0.00001]
""")
    st.write("""ค่าคงที่ 2.5 หมายถึง ถ้า Feature ทั้งหมดเป็น 0 ราคาหุ้นปิดจะมีค่า 2.5
ค่าสัมประสิทธิ์แต่ละตัวแสดงผลกระทบของ Feature ที่มีต่อราคาปิด เช่น
ถ้า Open เพิ่มขึ้น 1 หน่วย ราคาปิดจะเพิ่มขึ้น 0.8 หน่วย
ถ้า Volume เพิ่มขึ้น 1 หน่วย ราคาปิดจะลดลง 0.00001 หน่วย (ผลกระทบน้อย)
""")
    st.write("7. ทำนายราคาหุ้นบนชุดทดสอบ")
    st.code("""y_pred = model.predict(X_test)""")
    st.write("model.predict(X_test) ใช้ค่าที่โมเดลเรียนรู้มาทำนายราคาหุ้น")
    st.write("8. วัดความแม่นยำของโมเดล")
    st.code("""mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Mean Squared Error:", mse)
print("R-squared:", r2)
""")
    st.write("""&nbsp;&nbsp;&nbsp;&nbsp;
        mean_squared_error(y_test, y_pred) คำนวณค่า MSE เพื่อวัดค่าคลาดเคลื่อน
        r2_score(y_test, y_pred) คำนวณเพื่อดูว่าโมเดลอธิบายข้อมูลได้ดีแค่ไหน  ถ้า MSE มีค่าน้อย แสดงว่าโมเดลมีค่าคลาดเคลื่อนต่ำ
        ถ้า R^2 ใกล้ 1 แสดงว่าโมเดลสามารถอธิบายข้อมูลได้ดี""")
    st.write("ตัวอย่างผลลัพธ์ที่ได้")
    st.code("""Mean Squared Error: 3.25
        R-squared: 0.92
        """)
    st.write("R^2 = 0.92 หมายความว่า โมเดลสามารถอธิบายความแปรปรวนของราคาหุ้นได้ 92%")
    st.write("9. การวาดกราฟเปรียบเทียบค่าจริงกับค่าทำนาย")
    st.code("""plt.scatter(y_test, y_pred)
plt.xlabel("Actual Prices")
plt.ylabel("Predicted Prices")
plt.title("Actual vs Predicted Stock Prices")
plt.show()
""")
    st.write("วาดกราฟ Scatter Plot เพื่อดูว่า ค่าจริง (Actual) และ ค่าทำนาย (Predicted) ใกล้กันแค่ไหนถ้าค่ากระจุกตัวอยู่บนเส้นตรง แสดงว่าโมเดลทำงานได้ดี")
    st.write("")
    st.write("")


    ####ส่วนที่ 2 SVR
    st.header("Support Vector Regression (SVR)")
    st.image("https://i0.wp.com/spotintelligence.com/wp-content/uploads/2024/05/support-vector-regression-svr.jpg?resize=1024%2C576&ssl=1", caption="ขอขอบคุณรูปภาพจาก https://i0.wp.com/spotintelligence.com")
    st.write("""
    การทำนายราคาหุ้นเป็นปัญหาที่มีความซับซ้อนสูง เนื่องจากราคาหุ้นได้รับอิทธิพลจากปัจจัยหลายประการ เช่น 
    อุปสงค์และอุปทานในตลาด ข่าวสารเกี่ยวกับบริษัท และสภาวะเศรษฐกิจโดยรวม 
    โมเดลทางคณิตศาสตร์จึงถูกนำมาใช้เพื่อลดความซับซ้อนและช่วยให้เราสามารถคาดการณ์แนวโน้มของราคาในอนาคตได้ 

    Support Vector Regression (SVR) เป็นอัลกอริธึมที่พัฒนาต่อยอดมาจาก **Support Vector Machine (SVM)** 
    ซึ่งปกติแล้ว SVM จะใช้สำหรับการจำแนกประเภท (Classification) 
    แต่เมื่อเรานำแนวคิดนี้มาประยุกต์ใช้กับการพยากรณ์ค่าต่อเนื่อง ก็จะกลายเป็น **Support Vector Regression (SVR)**
    """)

    st.subheader("หลักการทำงานของ SVR")
    st.write("""
    1. **เส้น Hyperplane และ Margin (ε-tube)**  โมเดลพยายามทำให้ค่าพยากรณ์อยู่ภายในช่วงค่าคลาดเคลื่อนที่ยอมรับได้ (ε-tube)  
    2. **Support Vectors**  จุดข้อมูลที่อยู่ใกล้กับขอบของ Margin จะถูกเรียกว่า Support Vectors  
    3. **ค่า C (Regularization Parameter)**  กำหนดว่ารับ error ได้มากน้อยเพียงใด (ค่า C สูงแสดงว่าโมเดลพยายามลด error มากขึ้น)  
    4. **ค่า Epsilon (ε)**  กำหนดขนาดของ Margin (ε สูง แสดงว่าโมเดลยืดหยุ่นมากขึ้น)  
    5. **Kernel Trick**  ใช้สำหรับแปลงข้อมูลที่ซับซ้อนให้สามารถพยากรณ์ได้ดีขึ้น เช่น  
        - **Linear Kernel** - ข้อมูลที่มีความสัมพันธ์เชิงเส้น  
        - **Polynomial Kernel** - ข้อมูลที่มีรูปแบบโค้ง  
        - **RBF Kernel** - ข้อมูลที่มีความซับซ้อน  
    """)

    
    st.header("การพัฒนาโมเดล SVR")

    st.write("1. โหลดไลบรารีที่จำเป็น")
    st.write("ก่อนที่เราจะสร้างโมเดล Machine Learning เราต้องโหลดไลบรารีที่จำเป็น เช่น numpy, pandas, matplotlib และ sklearn")
    st.code("""
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from sklearn.svm import SVR
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_squared_error, r2_score
    """)

    st.write("2. โหลดข้อมูลและดูโครงสร้างของข้อมูล")
    st.write("เราจะโหลดข้อมูลราคาหุ้น Tesla จากไฟล์ CSV และดูตัวอย่างข้อมูล")
    st.code("""
    df = pd.read_csv("tesla_stock_data.csv")
    df.head()
    """)

    st.write("3. เลือก Features และ Target")
    st.write("""
    - X คือ ตัวแปรที่ใช้เป็น Input ได้แก่ **Open, High, Low, Volume**  
    - y คือ ค่าที่ต้องการทำนาย ได้แก่ **Close**  
    """)
    st.code("""
    X = df[['Open', 'High', 'Low', 'Volume']]
    y = df['Close']
    """)

    st.write("4. แบ่งข้อมูลเป็นชุด Train และ Test")
    st.write("""
    - เราแบ่งข้อมูลเป็น 80% สำหรับ Train และ 20% สำหรับ Test  
    - `random_state=42` เพื่อให้ผลลัพธ์คงที่ทุกครั้งที่รัน  
    """)
    st.code("""
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    """)

    st.write("5. ทำการ Scaling ข้อมูล")
    st.write("""
    เนื่องจาก SVR อ่อนไหวต่อขนาดของข้อมูล เราจึงต้อง **Standardize** ข้อมูลก่อนใช้งาน  
    """)
    st.code("""
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    """)

    st.write("6. สร้างโมเดล SVR และทำการ Train")
    st.write("""
    - เราใช้ **RBF Kernel** ซึ่งสามารถจับรูปแบบข้อมูลที่ซับซ้อนได้ดี  
    - C=100 → โมเดลพยายามลด error ให้มากที่สุด  
    - epsilon=0.1 → กำหนดช่วงค่าคลาดเคลื่อนที่ยอมรับได้  
    """)
    st.code("""
    svr = SVR(kernel='rbf', C=100, epsilon=0.1)
    svr.fit(X_train_scaled, y_train)
    """)

    st.subheader("7. ทำนายราคาหุ้นบนชุดทดสอบ")
    st.write("เมื่อนำข้อมูล X_test_scaled ไปผ่านโมเดล SVR จะได้ค่าทำนาย (y_pred)")
    st.code("""
    y_pred = svr.predict(X_test_scaled)
    """)

    st.subheader("8. วัดความแม่นยำของโมเดล")
    st.write("""
    เราวัดค่าความคลาดเคลื่อน (Mean Squared Error) และประสิทธิภาพของโมเดล (R-squared)  
    """)
    st.code("""
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print("Mean Squared Error:", mse)
    print("R-squared:", r2)
    """)

    st.subheader("9. การวาดกราฟเปรียบเทียบค่าจริงกับค่าทำนาย")
    st.write("""
    เราสามารถใช้ **scatter plot** เพื่อตรวจสอบว่าค่าที่โมเดลพยากรณ์ใกล้เคียงกับค่าจริงหรือไม่  
    """)
    st.code("""
    plt.scatter(y_test, y_pred)
    plt.xlabel("Actual Prices")
    plt.ylabel("Predicted Prices")
    plt.title("Actual vs Predicted Stock Prices")
    plt.show()
    """)

    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.header("แหล่งที่มา")
    st.write("""
1. Schölkopf, B., & Smola, A. J. (2002). *Learning with Kernels: Support Vector Machines, Regularization, Optimization, and Beyond.* MIT Press.  
2. Scikit-Learn. "sklearn.svm.SVR," Available: [Scikit-Learn Documentation](https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVR.html).  
3. Murphy, J. J. (1999). *Technical Analysis of the Financial Markets: A Comprehensive Guide to Trading Methods and Applications.* New York Institute of Finance.  
4. Investopedia. "How Stock Prices Are Determined," Available: [Investopedia](https://www.investopedia.com/articles/stocks/07/stock_price.asp).  
5. Pedregosa, F., et al. (2011). *Scikit-learn: Machine Learning in Python.* Journal of Machine Learning Research, 12, 2825-2830.  
6. Towards Data Science. "Stock Price Prediction using Support Vector Regression," Available: [Towards Data Science](https://towardsdatascience.com/stock-price-prediction-using-support-vector-regression-51f03dfe2db6).
7. การรวบรวมข้อมูลบางส่วนจาก ChatGPT(https://chatgpt.com).
8.แหล่งข้อมูลของ dataset. 
    - **แหล่งที่มา:** Yahoo Finance  
    - **เว็บไซต์:** [Yahoo Finance - Tesla (TSLA)](https://finance.yahoo.com/quote/TSLA/history)  
    - **รายละเอียด:** รวมราคาหุ้น Tesla รายวัน เช่น Open, High, Low, Close, Volume.  
""")
 
#####NN คำอธิบาย
elif page == "NN Description":
    st.title("การพยากรณ์ความเสี่ยงการเป็นโรคเบาหวานของผู้ป่วยด้วย Neural Network: การสร้างโมเดลด้วย MLP")

    st.header("Neural Network")
    st.write("""
    &nbsp;&nbsp;&nbsp;&nbsp;Neural Network หรือ โครงข่ายประสาทเทียม เป็นอัลกอริธึมที่ได้รับแรงบันดาลใจจากโครงสร้างของสมองมนุษย์ 
    โดยเซลล์ประสาทเทียม (Neuron) ในคอมพิวเตอร์จะทำหน้าที่คล้ายกับเซลล์ประสาทในสมอง คือรับข้อมูล ประมวลผล 
    และส่งสัญญาณไปยังเซลล์ถัดไป
    """)
    st.image("https://media.geeksforgeeks.org/wp-content/cdn-uploads/20230602113310/Neural-Networks-Architecture.png", caption="ขอบคุณรูปภาพจาก https://media.geeksforgeeks.org")

    st.write("""
    &nbsp;&nbsp;&nbsp;&nbsp;MLP (Multi-Layer Perceptron) เป็น Neural Network ประเภทหนึ่งที่มีหลายชั้น (Multi-layer) โดยมีองค์ประกอบหลักดังนี้:
    1. **Input Layer (ชั้นอินพุต)** → รับค่าคุณลักษณะ (Feature)
    2. **Hidden Layers (ชั้นซ่อนเร้น)** → ทำการประมวลผลข้อมูล
    3. **Output Layer (ชั้นผลลัพธ์)** → ให้คำตอบว่าเป็นเบาหวานหรือไม่
    """)

    st.subheader("ตัวอย่างโครงสร้างของโมเดลที่เราจะสร้าง")
    st.code("""
    Input Layer: 8 Neurons (1 Neuron ต่อ Feature)
    Hidden Layer 1: 64 Neurons, Activation = ReLU
    Hidden Layer 2: 32 Neurons, Activation = ReLU
    Hidden Layer 3: 16 Neurons, Activation = ReLU
    Output Layer: 1 Neuron, Activation = Sigmoid
    """)

    st.subheader("หลักการทำงานของ Neuron")
    st.write("""
    Neuron แต่ละตัวใน Hidden Layer ทำงานตาม 3 ขั้นตอนหลัก:

    1. **คำนวณค่าถ่วงน้ำหนักของอินพุต**
    """)

    st.code("""Z = (w1 * x1 + w2 * x2 + ... + wn * xn) + b""")

    st.write("""
    โดยที่:
    - **xᵢ** คือค่าคุณลักษณะ (Feature)
    - **wᵢ** คือน้ำหนัก (Weight)
    - **b** คือค่าคงที่ (Bias)
    """)

    st.write("""
    2. **ใช้ Activation Function เพื่อแปลงค่า Z เป็นค่าที่ไม่เป็นเชิงเส้น**
    """)

    st.code("""A = f(Z)""")

    st.write("""
    ซึ่ง ReLU และ Sigmoid เป็นฟังก์ชันที่ใช้ในโมเดลนี้
    """)

    st.write("""
    3. **ส่งค่าที่ผ่านการประมวลผลไปยัง Neuron ถัดไปหรือชั้นผลลัพธ์**
    """)

    st.subheader("แนวคิดและองค์ประกอบของ MLP")

    st.subheader("1. Activation Function")
    st.write("""
    ฟังก์ชันกระตุ้นช่วยให้โมเดลสามารถเรียนรู้รูปแบบที่ซับซ้อนได้ โดยโมเดลนี้ใช้:
    """)

    st.write("""
    **ReLU (Rectified Linear Unit)**
    """)

    st.code("""f(x) = max(0, x)""")

    st.write("""
    ถ้าค่า x เป็นบวก จะคืนค่า x
    ถ้า x เป็นลบ จะคืนค่า 0
    **ข้อดี:** ทำให้โมเดลเรียนรู้เร็วขึ้น และลดปัญหา Gradient Vanishing
    """)

    st.write("""
    **Sigmoid**
    """)

    st.code("""f(x) = 1 / (1 + e^(-x))""")

    st.write("""
    ค่าอินพุตถูกแปลงเป็นค่าระหว่าง 0 ถึง 1 ซึ่งเหมาะกับ Binary Classification
    """)

    st.subheader("2. Loss Function")
    st.write("""
    Binary Cross-Entropy Loss เป็นฟังก์ชันที่ใช้ในปัญหาการจำแนกประเภทแบบสองกลุ่ม:
    """)

    st.code("""Loss = -[y * log(y^) + (1 - y) * log(1 - y^)]""")

    st.write("""
    - ถ้า ค่า **ŷ** ใกล้ 1 แต่ y จริงเป็น 0 → ค่าความสูญเสียสูง (โมเดลพยากรณ์ผิด)
    - ถ้า ค่า **ŷ** ใกล้ 0 แต่ y จริงเป็น 1 → ค่าความสูญเสียสูง
    - ถ้า ค่า **ŷ** ใกล้กับ y จริง → ค่าความสูญเสียต่ำ (โมเดลพยากรณ์ถูกต้อง)
    """)

    st.subheader("การพัฒนาโมเดล")

    st.subheader("1 โหลดไลบรารีและข้อมูล")
    st.code("""
    import pandas as pd
    import numpy as np
    from sklearn.model_selection import train_test_split
    from sklearn.neural_network import MLPClassifier
    from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

    # โหลดข้อมูล
    data = pd.read_csv("diabetes.csv")
    print(data.head())
    """)

    
    st.write("นำเข้า library ต่าง ๆ สำหรับการเรียกใช้งาน จากนั้นดาวน์โหลด diabetes.csv และแสดงข้อมูล เพื่อตรวจสอบข้อมูล")

    st.subheader("2. ตรวจสอบข้อมูลและค่าที่หายไป")
    st.code("""print(data.isnull().sum())""")

    
    st.write("ตรวจสอบค่าที่หายไป หรือ mising value ใน เป็นหนึ่งในการเตรียมความพร้อมของข้อมูล เพื่อป้องกันการผิดพลาดที่จะเกิดขึ้นกับ model")

    st.subheader("3. แบ่งข้อมูลเป็น Feature และ Target")
    st.code("""
    X = data.drop("Outcome", axis=1)  # Feature
    y = data["Outcome"]  # Target
    """)

    
    st.write("""
    - **X** ใช้เก็บค่า feature
    - **y** ใช้เก็บค่า target (0 = ปกติ, 1 = เบาหวาน)
    """)

    st.subheader("4. แบ่งชุดข้อมูล Train/Test")
    st.code("""
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    """)

    
    st.write("แบ่งข้อมูล 80% สำหรับ Train และ 20% สำหรับ Test เพื่อเตรียมพร้อมสำหรับการ train model")

    st.subheader("5. สร้างและ Train โมเดล MLP")
    st.code("""
    model = MLPClassifier(
        hidden_layer_sizes=(64, 32, 16),
        activation="relu",
        solver="adam",
        max_iter=3000,
        learning_rate_init=0.01,
        alpha=0.00001
    )

    model.fit(X_train, y_train)
    """)

    
    st.write("""
    - สร้างโมเดล Neural Network ที่มี 3 layers
    - ใช้ **ReLU Activation** และ **Adam Optimizer**
             โดยเหตุผลที่ใช้ ReLU เพราะ ทำให้โมเดลเรียนรู้ได้เร็วและหลีกเลี่ยงปัญหา Gradient Vanishing และใช้ Adam เพราะ ทำให้การอัปเดตค่าถ่วงน้ำหนักมีประสิทธิภาพและเสถียร
    - เทรนโมเดล **3000 รอบ** เพื่อความแม่นยำของ model 
    """)

    st.subheader("6. ทดสอบโมเดลและวัดผลลัพธ์")
    st.code("""
    y_pred = model.predict(X_test)

    print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
    print(classification_report(y_test, y_pred))
    print(confusion_matrix(y_test, y_pred))
    """)

    
    st.write("""
    - ใช้โมเดลทำการ predict
    - แสดง **Accuracy, Precision, Recall, และ Confusion Matrix** เพื่อดึแนวโน้มความถูกต้องและความผิดพลาด หากมีข้อผิดพลาดมาก
             ก็จะทำการเทรนโมเดลเพิ่มเติม เพื่อให้โมเดลสามารถทำนายได้มีความแม่นยำมากขึ้น
    """)
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")

    st.header("แหล่งที่มา")
    st.write("""
    1. Developers Google. "Activation Functions," Available: [Google Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course/neural-networks/activation-functions?hl=th&utm_source=chatgpt.com).  
    2. Guopai Blog. "Adam Optimizer and its Benefits," Available: [Guopai Machine Learning Blog](https://guopai.github.io/ml-blog17.html?utm_source=chatgpt.com).  
    3. Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep Learning.* MIT Press.  
    4. Rumelhart, D. E., Hinton, G. E., & Williams, R. J. (1986). "Learning representations by back-propagating errors," *Nature*, 323(6088), 533-536.  
    5. Nielsen, M. A. (2015). *Neural Networks and Deep Learning.* Determination Press.  
    6. Scikit-Learn. "MLPClassifier," Available: [Scikit-Learn Documentation](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html).  
    7. การรวบรวมข้อมูลบางส่วนจาก ChatGPT(https://chatgpt.com).
    8. แหล่งที่มาของ dataset - **แหล่งที่มา:** Pima Indians Diabetes Database.  
        - **เว็บไซต์:** [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/Pima+Indians+Diabetes)  
        - **อ้างอิงจาก:** National Institute of Diabetes and Digestive and Kidney Diseases (NIDDK)  
        - **รายละเอียด:** ใช้ศึกษาความสัมพันธ์ระหว่างสุขภาพและโรคเบาหวาน.    
    """)
