import streamlit as st
from datetime import datetime
import json
import os

# 페이지 설정
st.set_page_config(
    page_title="🥛 우유 섭취 기록",
    page_icon="🥛",
    layout="centered"
)

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
st.markdown("**매일 목표량을 달성하고 등급을 올려보세요!**")

# 사이드바 - 설정
with st.sidebar:
    st.header("⚙️ 설정")
    daily_goal = st.number_input(
        "하루 목표량 (ml)", 
        min_value=100, 
        max_value=2000, 
        value=700, 
        step=10
    )
    st.markdown("---")
    st.markdown("### 📊 등급 시스템")
    st.markdown("""
    - 🥉 **브론즈**: 1일 연속
    - 🥈 **실버**: 3일 연속
    - 🥇 **골드**: 7일 연속
    - 💎 **다이아**: 30일 연속
    """)

# 메인 영역
tab1, tab2 = st.tabs(["📝 기록하기", "📈 통계"])

with tab1:
    st.header("오늘의 우유 기록")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # 이미지 업로드
        uploaded_file = st.file_uploader(
            "우유 사진 찍기 📸", 
            type=['jpg', 'jpeg', 'png']
        )
        
        if uploaded_file is not None:
            st.image(uploaded_file, caption="업로드된 사진", use_column_width=True)
    
    with col2:
        # 수동 입력
        st.markdown("#### 섭취량 입력")
        milk_amount = st.number_input(
            "우유 양 (ml)", 
            min_value=0, 
            max_value=1000, 
            value=200, 
            step=50,
            key="milk_input"
        )
        
        memo = st.text_input("메모 (선택)", placeholder="예: 아침 식사와 함께")
        
        if st.button("✅ 기록하기", type="primary", use_container_width=True):
            if uploaded_file is not None or milk_amount > 0:
                # 새 기록 추가
                new_record = {
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "time": datetime.now().strftime("%H:%M"),
                    "amount": milk_amount,
                    "memo": memo,
                    "has_image": uploaded_file is not None
                }
                
                st.session_state.records.append(new_record)
                save_data(st.session_state.records)
                
                st.success(f"✅ {milk_amount}ml 기록 완료!")
                st.balloons()
            else:
                st.warning("사진을 업로드하거나 양을 입력해주세요!")
    
    # 오늘의 진행률
    st.markdown("---")
    st.markdown("### 오늘의 진행률")
    
    today = datetime.now().strftime("%Y-%m-%d")
    today_records = [r for r in st.session_state.records if r['date'] == today]
    today_total = sum(r['amount'] for r in today_records)
    
    progress = min(today_total / daily_goal, 1.0)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("오늘 섭취량", f"{today_total} ml")
    with col2:
        st.metric("목표량", f"{daily_goal} ml")
    with col3:
        percentage = int(progress * 100)
        st.metric("달성률", f"{percentage}%")
    
    st.progress(progress)
    
    if progress >= 1.0:
        st.success("🎉 오늘 목표 달성! 축하합니다!")
    elif progress >= 0.7:
        st.info(f"💪 조금만 더! {daily_goal - today_total}ml 남았어요")
    
    # 오늘의 기록 목록
    if today_records:
        st.markdown("---")
        st.markdown("### 오늘의 기록")
        for i, record in enumerate(reversed(today_records)):
            with st.expander(f"🥛 {record['time']} - {record['amount']}ml"):
                if record.get('memo'):
                    st.write(f"📝 {record['memo']}")
                if record.get('has_image'):
                    st.write("📸 사진 있음")

with tab2:
    st.header("📈 나의 통계")
    
    if st.session_state.records:
        # 총 통계
        total_amount = sum(r['amount'] for r in st.session_state.records)
        total_days = len(set(r['date'] for r in st.session_state.records))
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("총 섭취량", f"{total_amount:,} ml")
        with col2:
            st.metric("기록 일수", f"{total_days} 일")
        with col3:
            avg = total_amount / total_days if total_days > 0 else 0
            st.metric("평균 섭취량", f"{int(avg)} ml/일")
        
        # 연속 달성일 계산
        st.markdown("---")
        st.markdown("### 🏆 현재 등급")
        
        # 간단한 연속 달성일 계산 (실제로는 더 복잡한 로직 필요)
        dates_with_goal = []
        for date in set(r['date'] for r in st.session_state.records):
            day_total = sum(r['amount'] for r in st.session_state.records if r['date'] == date)
            if day_total >= daily_goal:
                dates_with_goal.append(date)
        
        streak_days = len(dates_with_goal)
        
        # 등급 결정
        if streak_days >= 30:
            rank = "💎 다이아몬드"
            rank_color = "#00D4FF"
        elif streak_days >= 7:
            rank = "🥇 골드"
            rank_color = "#FFD700"
        elif streak_days >= 3:
            rank = "🥈 실버"
            rank_color = "#C0C0C0"
        elif streak_days >= 1:
            rank = "🥉 브론즈"
            rank_color = "#CD7F32"
        else:
            rank = "🌱 새싹"
            rank_color = "#90EE90"
        
        st.markdown(f"## {rank}")
        st.markdown(f"**연속 달성일: {streak_days}일**")
        
        # 다음 등급까지
        if streak_days < 3:
            next_goal = 3 - streak_days
            st.info(f"🥈 실버까지 {next_goal}일 남았어요!")
        elif streak_days < 7:
            next_goal = 7 - streak_days
            st.info(f"🥇 골드까지 {next_goal}일 남았어요!")
        elif streak_days < 30:
            next_goal = 30 - streak_days
            st.info(f"💎 다이아까지 {next_goal}일 남았어요!")
        else:
            st.success("🎉 최고 등급 달성! 계속 유지하세요!")
        
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
            st.write(f"{achieved} **{date}**: {amount}ml / {daily_goal}ml")
        
    else:
        st.info("아직 기록이 없습니다. 첫 기록을 추가해보세요! 🥛")

# 하단 정보
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 0.9em;'>
    💡 매일 우유를 마시고 건강을 챙기세요!<br>
    문의사항이 있으시면 Claude에게 물어보세요 😊
    </div>
    """, 
    unsafe_allow_html=True
)
