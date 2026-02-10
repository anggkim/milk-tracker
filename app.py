import streamlit as st
from datetime import datetime
import json
import os

# 페이지 설정
st.set_page_config(
    page_title="🥛 우유 섭취 기록",
    page_icon="🥛",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS 스타일
st.markdown("""
<style>
    /* 전체 배경 그라데이션 */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* 메인 컨테이너 스타일 */
    .main .block-container {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    
    /* 제목 스타일 */
    h1 {
        color: #667eea;
        text-align: center;
        font-size: 3em !important;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        animation: fadeIn 1s ease-in;
    }
    
    /* 애니메이션 정의 */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    /* 카드 스타일 */
    .stMetric {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        animation: slideIn 0.5s ease-out;
        transition: transform 0.3s ease;
    }
    
    .stMetric:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-size: 1.1em;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        animation: pulse 2s infinite;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
        animation: none;
    }
    
    /* 프로그레스 바 스타일 */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        border-radius: 10px;
        height: 20px;
    }
    
    /* 사이드바 스타일 */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .css-1d391kg h2, [data-testid="stSidebar"] h2 {
        color: white !important;
    }
    
    .css-1d391kg .stMarkdown, [data-testid="stSidebar"] .stMarkdown {
        color: white !important;
    }
    
    /* 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f5f7fa;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #e0e7ff;
        transform: translateY(-2px);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
    }
    
    /* 확장 패널 스타일 */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 10px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%);
        transform: translateX(5px);
    }
    
    /* 등급 배지 스타일 */
    .rank-badge {
        font-size: 4em;
        text-align: center;
        padding: 20px;
        border-radius: 20px;
        margin: 20px 0;
        animation: pulse 2s infinite;
    }
    
    .rank-bronze {
        background: linear-gradient(135deg, #CD7F32 0%, #E6A85C 100%);
        box-shadow: 0 0 30px rgba(205, 127, 50, 0.5);
    }
    
    .rank-silver {
        background: linear-gradient(135deg, #C0C0C0 0%, #E8E8E8 100%);
        box-shadow: 0 0 30px rgba(192, 192, 192, 0.5);
    }
    
    .rank-gold {
        background: linear-gradient(135deg, #FFD700 0%, #FFED4E 100%);
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.5);
    }
    
    .rank-diamond {
        background: linear-gradient(135deg, #00D4FF 0%, #7DEDFF 100%);
        box-shadow: 0 0 40px rgba(0, 212, 255, 0.7);
        animation: pulse 1s infinite;
    }
    
    /* 성공 메시지 스타일 */
    .stSuccess {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border-left: 5px solid #10b981;
        border-radius: 10px;
        animation: slideIn 0.5s ease-out;
    }
    
    /* 정보 메시지 스타일 */
    .stInfo {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border-left: 5px solid #3b82f6;
        border-radius: 10px;
    }
    
    /* 입력 필드 스타일 */
    .stNumberInput > div > div > input,
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e5e7eb;
        transition: all 0.3s ease;
    }
    
    .stNumberInput > div > div > input:focus,
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* 파일 업로더 스타일 */
    .stFileUploader {
        border: 2px dashed #667eea;
        border-radius: 15px;
        padding: 20px;
        background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        border-color: #764ba2;
        background: linear-gradient(135deg, #e0e7ff 0%, #ddd6fe 100%);
    }
</style>
""", unsafe_allow_html=True)

# 데이터 파일 경로
DATA_FILE = "milk_records.json"

# 데이터 로드 함수
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# 데이터 저장 함수
def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 데이터 로드
if 'records' not in st.session_state:
    st.session_state.records = load_data()

# 앱 제목
st.title("🥛 우유 섭취 기록 앱")
st.markdown("""
<div style='text-align: center; color: #667eea; font-size: 1.2em; margin-bottom: 2rem;'>
    <b>✨ 매일 목표량을 달성하고 등급을 올려보세요! ✨</b>
</div>
""", unsafe_allow_html=True)

# 사이드바 - 설정
with st.sidebar:
    st.header("⚙️ 설정")
    daily_goal = st.number_input(
        "🎯 하루 목표량 (ml)", 
        min_value=100, 
        max_value=2000, 
        value=500, 
        step=50
    )
    st.markdown("---")
    st.markdown("### 🏆 등급 시스템")
    st.markdown("""
    <div style='color: white; line-height: 2;'>
    🥉 <b>브론즈</b>: 1일 연속<br>
    🥈 <b>실버</b>: 3일 연속<br>
    🥇 <b>골드</b>: 7일 연속<br>
    💎 <b>다이아</b>: 30일 연속
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <div style='color: white; font-size: 0.9em; text-align: center;'>
    💡 건강한 하루를 위해<br>우유를 마셔요!
    </div>
    """, unsafe_allow_html=True)

# 메인 영역
tab1, tab2 = st.tabs(["📝 기록하기", "📈 통계 보기"])

with tab1:
    st.markdown("### 🌟 오늘의 우유 기록")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 📸 사진 업로드")
        uploaded_file = st.file_uploader(
            "우유 사진을 찍어주세요!", 
            type=['jpg', 'jpeg', 'png'],
            label_visibility="collapsed"
        )
        
        if uploaded_file is not None:
            st.image(uploaded_file, caption="✨ 업로드된 사진", use_column_width=True)
            st.markdown("""
            <div style='text-align: center; color: #10b981; font-weight: bold; margin-top: 10px;'>
            ✅ 사진 업로드 완료!
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 💧 섭취량 입력")
        milk_amount = st.number_input(
            "우유 양 (ml)", 
            min_value=0, 
            max_value=1000, 
            value=200, 
            step=50,
            key="milk_input",
            label_visibility="collapsed"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        memo = st.text_input("📝 메모 (선택사항)", placeholder="예: 아침 식사와 함께 마셨어요")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("✅ 기록하기", type="primary", use_container_width=True):
            if uploaded_file is not None or milk_amount > 0:
                new_record = {
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "time": datetime.now().strftime("%H:%M"),
                    "amount": milk_amount,
                    "memo": memo,
                    "has_image": uploaded_file is not None
                }
                
                st.session_state.records.append(new_record)
                save_data(st.session_state.records)
                
                st.success(f"🎉 {milk_amount}ml 기록 완료!")
                st.balloons()
                st.snow()
            else:
                st.warning("⚠️ 사진을 업로드하거나 양을 입력해주세요!")
    
    # 오늘의 진행률
    st.markdown("---")
    st.markdown("### 📊 오늘의 진행률")
    
    today = datetime.now().strftime("%Y-%m-%d")
    today_records = [r for r in st.session_state.records if r['date'] == today]
    today_total = sum(r['amount'] for r in today_records)
    
    progress = min(today_total / daily_goal, 1.0)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💧 오늘 섭취량", f"{today_total} ml")
    with col2:
        st.metric("🎯 목표량", f"{daily_goal} ml")
    with col3:
        percentage = int(progress * 100)
        st.metric("📈 달성률", f"{percentage}%")
    
    st.progress(progress)
    
    if progress >= 1.0:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); 
                    padding: 20px; border-radius: 15px; text-align: center; 
                    font-size: 1.2em; font-weight: bold; color: #065f46; margin: 20px 0;
                    animation: pulse 1s infinite;'>
        🎉 오늘 목표 달성! 정말 잘하셨어요! 🎉
        </div>
        """, unsafe_allow_html=True)
    elif progress >= 0.7:
        st.info(f"💪 거의 다 왔어요! {daily_goal - today_total}ml만 더 마시면 달성!")
    elif progress > 0:
        st.info(f"🏃‍♂️ 좋아요! {daily_goal - today_total}ml 남았어요, 화이팅!")
    else:
        st.info("🌅 오늘도 화이팅! 첫 우유를 기록해보세요!")
    
    # 오늘의 기록 목록
    if today_records:
        st.markdown("---")
        st.markdown("### 📋 오늘의 기록 내역")
        for i, record in enumerate(reversed(today_records)):
            with st.expander(f"🥛 {record['time']} - {record['amount']}ml", expanded=(i==0)):
                col1, col2 = st.columns([3, 1])
                with col1:
                    if record.get('memo'):
                        st.write(f"📝 **메모:** {record['memo']}")
                    else:
                        st.write("📝 메모 없음")
                with col2:
                    if record.get('has_image'):
                        st.markdown("""
                        <div style='text-align: center; color: #667eea; font-weight: bold;'>
                        📸<br>사진 있음
                        </div>
                        """, unsafe_allow_html=True)

with tab2:
    st.markdown("### 📈 나의 통계")
    
    if st.session_state.records:
        # 총 통계
        total_amount = sum(r['amount'] for r in st.session_state.records)
        total_days = len(set(r['date'] for r in st.session_state.records))
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🥛 총 섭취량", f"{total_amount:,} ml")
        with col2:
            st.metric("📅 기록 일수", f"{total_days} 일")
        with col3:
            avg = total_amount / total_days if total_days > 0 else 0
            st.metric("📊 평균 섭취량", f"{int(avg)} ml/일")
        
        # 연속 달성일 계산
        st.markdown("---")
        
        dates_with_goal = []
        for date in set(r['date'] for r in st.session_state.records):
            day_total = sum(r['amount'] for r in st.session_state.records if r['date'] == date)
            if day_total >= daily_goal:
                dates_with_goal.append(date)
        
        streak_days = len(dates_with_goal)
        
        # 등급 결정
        if streak_days >= 30:
            rank = "💎 다이아몬드"
            rank_class = "rank-diamond"
            rank_emoji = "💎"
        elif streak_days >= 7:
            rank = "🥇 골드"
            rank_class = "rank-gold"
            rank_emoji = "🥇"
        elif streak_days >= 3:
            rank = "🥈 실버"
            rank_class = "rank-silver"
            rank_emoji = "🥈"
        elif streak_days >= 1:
            rank = "🥉 브론즈"
            rank_class = "rank-bronze"
            rank_emoji = "🥉"
        else:
            rank = "🌱 새싹"
            rank_class = "rank-bronze"
            rank_emoji = "🌱"
        
        st.markdown(f"""
        <div class='rank-badge {rank_class}'>
            <div style='font-size: 2em;'>{rank_emoji}</div>
            <div style='font-size: 0.5em; margin-top: 10px; color: white; font-weight: bold;'>{rank}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style='text-align: center; font-size: 1.3em; font-weight: bold; color: #667eea; margin: 20px 0;'>
        🔥 연속 달성일: {streak_days}일
        </div>
        """, unsafe_allow_html=True)
        
        # 다음 등급까지
        if streak_days < 3:
            next_goal = 3 - streak_days
            st.info(f"🥈 실버까지 {next_goal}일 남았어요! 조금만 더 화이팅!")
        elif streak_days < 7:
            next_goal = 7 - streak_days
            st.info(f"🥇 골드까지 {next_goal}일 남았어요! 거의 다 왔어요!")
        elif streak_days < 30:
            next_goal = 30 - streak_days
            st.info(f"💎 다이아까지 {next_goal}일 남았어요! 최고 등급까지!")
        else:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #00D4FF 0%, #7DEDFF 100%); 
                        padding: 20px; border-radius: 15px; text-align: center; 
                        font-size: 1.2em; font-weight: bold; color: white; margin: 20px 0;
                        box-shadow: 0 0 40px rgba(0, 212, 255, 0.5);'>
            🎉 최고 등급 달성! 당신은 우유 마스터! 🎉
            </div>
            """, unsafe_allow_html=True)
        
        # 최근 7일 기록
        st.markdown("---")
        st.markdown("### 📅 최근 7일 기록")
        
        from collections import defaultdict
        daily_totals = defaultdict(int)
        for record in st.session_state.records:
            daily_totals[record['date']] += record['amount']
        
        recent_dates = sorted(daily_totals.keys(), reverse=True)[:7]
        
        for date in recent_dates:
            amount = daily_totals[date]
            achieved = "✅" if amount >= daily_goal else "⏳"
            percentage = min(int((amount / daily_goal) * 100), 100)
            
            # 프로그레스 바 색상 결정
            if percentage >= 100:
                color = "#10b981"
            elif percentage >= 70:
                color = "#3b82f6"
            else:
                color = "#f59e0b"
            
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); 
                        padding: 15px; border-radius: 10px; margin: 10px 0;'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <span style='font-weight: bold;'>{achieved} {date}</span>
                    <span style='color: {color}; font-weight: bold;'>{amount}ml / {daily_goal}ml ({percentage}%)</span>
                </div>
                <div style='background: #e5e7eb; border-radius: 10px; height: 10px; margin-top: 10px; overflow: hidden;'>
                    <div style='background: {color}; height: 100%; width: {percentage}%; border-radius: 10px; transition: width 0.5s ease;'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
    else:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); 
                    padding: 40px; border-radius: 15px; text-align: center; margin: 20px 0;'>
            <div style='font-size: 4em;'>🥛</div>
            <div style='font-size: 1.2em; font-weight: bold; color: #1e40af; margin-top: 20px;'>
            아직 기록이 없습니다<br>첫 우유를 기록해보세요!
            </div>
        </div>
        """, unsafe_allow_html=True)

# 하단 정보
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9em; padding: 20px;'>
    💡 매일 우유를 마시고 건강을 챙기세요!<br>
    <span style='color: #667eea; font-weight: bold;'>Made with ❤️ by Claude</span><br>
    <small>궁금한 점이 있으시면 Claude에게 물어보세요! 😊</small>
</div>
""", unsafe_allow_html=True)
