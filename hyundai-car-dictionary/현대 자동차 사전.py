import os
import json
from tkinter import *
from tkinter import ttk

# ----------------------------
# App
# ----------------------------
class HyundaiCarDictionary: # 현대차 사전 앱의 설계도(클래스). 인스턴스를 만들면 __init__이 실행되며 앱 초기 설정을 준비한다.
    def __init__(self): #생성자
        self.BASE_DIR = os.path.dirname(__file__) # 현재 파일(__file__)이 들어있는 폴더 경로(프로젝트 기준 경로) => BASE_DIR
        self.LOGO_PATH = os.path.join(self.BASE_DIR, "assets", "hyundai_logo.png") # 로고 이미지 파일 경로를 만들어 저장(나중에 로딩할 때 사용)
        self.DATA_DIR = os.path.join(self.BASE_DIR, "data_Hyundai") # 차량 데이터 폴더 경로(BASE_DIR + data_Hyundai)를 만들어 저장(데이터 탐색/로딩 기준 폴더)

        self.BG = "#FFFFFF" #배경색을 흰색으로 쓴다(나중에 실행 때 사용)

        self.window = Tk() #나중에( __init__)실행을 하게 되면 창을 띄움
        self.window.title("Hyundai Car Dictionary") #나중에( __init__) 실행하게 되면 창 제목 설정
        self.window.geometry("800x800") #나중에( __init__) 실행하게 되면 창 크기 설정
        self.window.configure(bg=self.BG) #나중에(__init__) 실행하게 되면  배경 색을 BG로 바꿈

        # 화면 컨테이너(여기에 home/list/detail을 올려두고 raise로 전환)
        self.container = Frame(self.window, bg=self.BG) #home/list/detail 같은 페이지들을 올려놓는 container를 만든다. (container = 같은 공간) 
        self.container.pack(fill="both", expand=True) #그 3개의 창들이 창 크기에 따라 같이 변함
        self.container.rowconfigure(0, weight=1) # 격자를 그려서 세밀하게 위치 조정 -> row는 행의 위치 조정, weight=1은 창 크기 변하면 이 칸이 늘어나라
        self.container.columnconfigure(0, weight=1) # 격자를 그려서 세밀하게 위치 조정 -> column는 열의 위치 조정, weight=1은 창 크기 변하면 이 칸이 늘어나라

        # 상태값(상세화면 사진 넘기기에 사용)
        self.detail_images = [] #나중에 실행할 때 상세 화면에서 사용할 이미지를 담아둘 리스트
        self.detail_img_idx = 0 #나중에 실행할 때 상세 이미지 리스트에서 현재 보여줄 이미지의 인덱스(0부터 시작)
        self.detail_photo = None  # PhotoImage 참조 유지, 나중에 실행할 때 상세 페이지에 띄울 PhotoImage를 저장해둘 변수를 만든다

        # 변수
        self.fuel_var = StringVar(value=" ")
        #StringVar() : Tkinter 전용 “문자열 변수” 객체 일반 파이썬 문자열이 아니라
        #StringVar()는 라디오버튼이 선택될 때 그 라디오버튼의 value 문자열을 “저장”해두는 상태 변수

        # 화면 만들기
        self._build_home() #나중에 실행할 때 홈 화면 Frame 만들기
        self._build_list() #나중에 실행할 때 리스트화면 (2번째) Frame 만들기
        self._build_detail() #나중에 실행할 때 상세화면(3번째) Frame 만들기

        self.show_frame(self.home_frame) #나중에 실행할 때 첫 화면을 home_frame으로 보여줘라

    # ----------------------------
    # UI 구성
    # ----------------------------
    def _build_home(self): #홈 화면 설계 함수
        self.home_frame = Frame(self.container, bg=self.BG) #container(공용 무대) 안에 홈 페이지용 Frame을 만들고 배경색을 BG로 설정
        self.home_frame.grid(row=0, column=0, sticky="nsew")
        #home_frame을 container의 (0,0) 칸에 배치하고, 창 크기 변화에 맞춰 상하좌우로 꽉 채우게 함(sticky=nsew)

        inner = Frame(self.home_frame, bg=self.BG) #home_frame 내부에 여백/레이아웃 관리를 위한 내부 컨테이너(inner) 생성
        inner.pack(fill="both", expand=True, padx=10, pady=10) # 안쪽에 붙이기 (home_frame의 크기가 변할때 마다 inner의 크기도 같이 변하게 설정)
                                                                                                # inner를 home_frame 안에서 최대한 크게 배치하고, 바깥쪽에 10px 여백(padx/pady)을 둠
                
        Label(inner, text="현대 자동차 검색", fg="black", bg=self.BG, #inner에 text = "현대 자동차 검색" 설정 및 색깔, 배경색, font, 여백 설정 후 붙인다
              font=("맑은 고딕", 18, "bold")).pack(pady=(10, 10))

        self.logo_img = PhotoImage(file=self.LOGO_PATH) #나중에 실행할 때 file=self.LOGO_PATH경로를 통해 이미지 불러 logo_img에 저장
        Label(inner, image=self.logo_img, bg=self.BG).pack(fill = "both", expand=True) # inner에 self.logo_img를 이미지화 시켜 라벨로 표시하고  배경색 설정 후 남는 공간을 받아 중앙에 가깝게 배치(expand=True)

        # 라디오 버튼
        radio_box = Frame(inner, bg=self.BG) #라디오 버튼을 만들기 위한 Frame(공간)을 만든다
        radio_box.pack(pady=10, anchor = 'center') # radio_box를 배치하고 위/아래 바깥 여백을 10px 줌

        Radiobutton(radio_box, text="가솔린", value="gasoline", variable=self.fuel_var, bg=self.BG).pack(side="left", padx=10)
        #라디오 박스에 라디오 버튼 생성, 글씨는 "가솔린",
        #이 버튼이 선택되면 self.fuel_var에 "gasoline"이 저장됨(value), 배경 설정 후
        #왼쪽에서 부터 차례대로 여백 10만큼 띄우면서 배치
        Radiobutton(radio_box, text="디젤", value="diesel", variable=self.fuel_var, bg=self.BG).pack(side="left", padx=10)
        Radiobutton(radio_box, text="전기차", value="electric", variable=self.fuel_var, bg=self.BG).pack(side="left", padx=10)

        ttk.Button(inner, text="시작", command=self.go_list_screen).pack(pady=10)
        #ttk.Button을 위 아래로 여백 10주면서 inner에 배치, 글씨는 '시작', 버튼을 누르게 되면  go_list_screen 함수 명령 실행
        Label(inner, text="Mini Project : 이상영", fg="black", bg=self.BG,
              font=("맑은 고딕", 16, "bold")).place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")
        # inner에 text 배치 하지만 정확한 위치로 배치(relx, rely = 1.0 = 아래 위치, se 남동쪽, 가로 세로 여백 12만큼 설정)
        
    def _build_list(self): #list 화면 설계 함수
        self.list_frame = Frame(self.container, bg=self.BG) # container 안에 배경색과 함께 Frame을 생성 -> list_frame
        self.list_frame.grid(row=0, column=0, sticky="nsew") #list_frame을 container의 (0,0) 칸에 배치하고, 창 크기 변화에 맞춰 상하좌우로 꽉 채우게 함(sticky=nsew)

        Label(self.list_frame, text="차종 목록", font=("맑은 고딕", 16, "bold"), bg=self.BG).pack(anchor="w", padx=10, pady=10)
        # 나중에 실행하게 되면 list_frame에 "차종 목록" 글씨를 font와 배경을 설정한 후 w 방향에 여백 가로,세로 위, 아래 10만큼 준 후 배치
        
        # Listbox + Scrollbar (차종 많을 때 필수)
        box = Frame(self.list_frame, bg=self.BG) #list_frame안에 Frame을 배경색과 함께 하나 더 형성 => box
        box.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        #box를 최대한 크게 붙이고 남는
        #expand = True : 공간이 있으면 box가 그 공간을 가져감 (커짐), 좌우 여백 10, 아래만 여백 10

        self.sb = ttk.Scrollbar(box, orient="vertical") # 나중에 실행하게 되면 ttk.Scrollbar를 box에 수직방향으로 설정할 것 => sb
        self.sb.pack(side="right", fill="y") # sb를 오른쪽 세로 방향으로 꽉 채우게 배치

        self.models_listbox = Listbox(box, height=20, yscrollcommand=self.sb.set)
        #box에 목록을 만들건데 최대 20개 까지 보이게 설정
        #리스트가 움직이면 스크롤바 표시가 따라감
        
        self.models_listbox.pack(side="left", fill="both", expand=True)
        #models_listbox를 왼쪽에 배치(오른쪽은 스크롤 바, 창 크기에 맞춰 최대한 크게 배치)
        
        self.sb.configure(command=self.models_listbox.yview) #스크롤바를 움직이면 리스트박스가 같이 움직이도록 연결합니다.

        ttk.Button(self.list_frame, text="이전", command=self.go_home_screen).pack(anchor="w", padx=10, pady=10)
        #list_frame에서 "이전" 글씨가 적힌 ttk.Button을 만들고 "이전을 클릭하면 home_screen으로 넘어가는 함수가 실행
        #'w'방향으로 여백 아래,위,좌,우 10 설정
        
        # 더블클릭/엔터로 상세 이동
        self.models_listbox.bind("<Double-Button-1>", self.open_detail) # 왼쪽 버튼을 더블 클릭하면 open_detail 폴더가 열린다
        self.models_listbox.bind("<Return>", self.open_detail) # 엔터를 누르면 open_detail 폴더가 열린다

    def _build_detail(self): # 상세 페이지 설계 함수
        self.detail_frame = Frame(self.container, bg=self.BG) #container 안에 배경색을 설정하여 Frame을 형성한다 => detail_frame
        self.detail_frame.grid(row=0, column=0, sticky="nsew")
        #detail_frame을 container의 (0,0) 칸에 배치하고, 창 크기 변화에 맞춰 상하좌우로 꽉 채우게 함(sticky=nsew)

        self.detail_title = Label(self.detail_frame, text="상세",font=("맑은 고딕", 16, "bold"), bg=self.BG)
        # detail_frame에 "상세" 글 표시, font 설정, 배경색 설정 => detail_title
        self.detail_title.pack(anchor="w", padx=10, pady=(10, 5))
        #detail_title을 왼쪽에 좌,우로 여백 10, 위 10, 아래 5의 여백을 주면서 배치
        ttk.Button(self.detail_frame, text="목록으로", command=self.go_back_to_list).pack(anchor="w", padx=10, pady=10)
        #detail_frame에 "목록으로" 글씨가 써진 ttk.Button 버튼 생성
        #버튼을 누르면 리스트 화면으로 넘어가는 함수 실행
        #버튼의 위치는 왼쪽으로 정렬하고 좌,우,위,아래 여백 10만큼 주면서 배치

        self.detail_img_label = Label(self.detail_frame, bg=self.BG)
        #detail_frame 안에 이미지(또는 사진)를 보여줄 Label 위젯을 하나 만들고,
        #그 Label의 배경색을 흰색으로 설정=> detail_img_label
        self.detail_img_label.pack(padx=10, pady=10)
        #detail_img_label을 좌,우.위,아래 10만큼 여백 주면서 배치
        
        self.detail_spec = Text(self.detail_frame, height=14)
        #detail_frame에 상세 정보를 입력하는 Text 구성, 최대 14줄이 보이도록 설정 => detail_spec
        self.detail_spec.pack(fill="both", expand=True, padx=10, pady=10)
        # detail_spec를 창이 꽉차고 남은 여백은 가져갈 수 있도록 설정하고 좌,우,위,아래 여백 10만큼 주면서 배치
        
        btn_detail_box = Frame(self.detail_frame, bg=self.BG)
        # detail_frame에 배경색을 설정하여 Frame 형성 => detail_box
        btn_detail_box.pack(anchor="center") # 그 detail_box를 중앙에 배치

        ttk.Button(btn_detail_box, text="◀ 이전 사진", command=self.prev_detail_image).pack(side="left", padx=10)
        #btn_detail_box에 "이전 사진"이라고 글씨가 적힌 ttk.Button를 생성하고
        #클릭하면 prev._detail_image 함수 실행
        #왼쪽부터 정렬하며 다음 버튼과 10의 여백이 존재
        ttk.Button(btn_detail_box, text="다음 사진 ▶", command=self.next_detail_image).pack(side="left", padx=10)
        
    def prev_detail_image(self): #상세 페이지에서 이전 버튼을 누르면 image가 이전으로 가는 함수
        self.change_image(-1)

    def next_detail_image(self): #상세 페이지에서 다음 버튼을 누르면 image가 다음으로 가는 함수
        self.change_image(1)
        
    # ----------------------------
    # 화면 전환
    # ----------------------------
    def show_frame(self, frame): 
        frame.tkraise()
    # (container에 겹쳐 올려둔) frame을 맨 위로 올려 보여줌
    
    def go_home_screen(self): 
        self.show_frame(self.home_frame)
    # 나중에 실행을 하게 되면 home_frame으로 설정

    def go_list_screen(self):
        fuel = self.fuel_var.get()
        self.load_models(fuel)
        self.show_frame(self.list_frame)
    # 사용자가 선택을 하는 연료가 fuel_var에 저장되고 .get로 그 정보를 가져와서 저장 => fuel
    # fuel에 담긴 정보로 부터 내가 저장한 모델들을 불러옴(해당 연료에 맞는 차종 목록을 읽어서 Listbox에 채운다)
    # list_frame의화면이 맨 위로 올라옴
    
    def go_back_to_list(self):
        self.show_frame(self.list_frame)
    # 상세 화면에서 목록 버튼 누르면 리스트 화면으로 되돌아 오는 함
    
    # ----------------------------
    # 데이터 로딩 유틸
    # ----------------------------
    def fuel_dir(self, fuel):
        return os.path.join(self.DATA_DIR, fuel)
    # 연료별 폴더 경로(DATA_DIR/fuel)를 조합해서 반환
    
    def model_dir(self, fuel, model_name):
        return os.path.join(self.DATA_DIR, fuel, model_name)
    # 특정 연료의 특정 차종 폴더 경로(DATA_DIR/fuel/model_name)를 만들어 반환
    
    def list_models(self, fuel):  # 연료에 따른 차량을 리스트에 올리는 함수
        fuel_path = self.fuel_dir(fuel) # # DATA_DIR 아래 fuel 폴더 경로를 조합해서 fuel_path에 저장 (예: .../data_Hyundai/gasoline)
        if not os.path.isdir(fuel_path): #만약 fuel path가 없다면?(isdir -> 진짜 경로가 있는지 없는지 검사하는 함수)
            return None, fuel_path # 폴더가 없으니 목록 대신 None을 주고, 문제 경로(fuel_path)도 함께 반환

        cars = os.listdir(fuel_path) #fuel path를 통해서 폴더 안에 있는 차량 이름을 가져와서 저장 => cars
        folders = [n for n in cars if os.path.isdir(os.path.join(fuel_path, n))]
        #cars 중에서 “폴더인 것만” 골라서 folders 리스트로 만든다
        return sorted(folders), fuel_path
        # 그  폴더들만 골라서 알파벳/가나다로 정렬하여 반환
        
    def read_spec(self, model_path): #특정 차량의 폴더 안에서 스펙을 찾아 읽는 함수
        """spec.json(우선) -> spec.txt -> 폴더 내 아무 txt 순으로 읽기"""
        spec_json = os.path.join(model_path, "spec.json") #우선 spec.json 파일을 읽어서 그 경로를  저장 => spec_json
        spec_txt = os.path.join(model_path, "spec.txt") # spec.txt 파일을 읽어서 그 경로를  저장=> spec_txt

        if os.path.exists(spec_json): #만약 spec_json의 경로로 읽고 싶다면
            try:
                with open(spec_json, "r", encoding="utf-8") as f:
                    # spec_json 파일을 읽기모드(r)로 연다
                    # encoding utf-8을 지정해서 한글도 읽을 수 있게 한다
                    # with as f문을 사용하면 블록이 끝날 때 파일이 자동으로 닫힌다(파일 열때는 with는 필수)
                    return ("json", json.load(f)) #json으로 반환
            except Exception as e: #예외가 일어날 시 오류 문구를 나타내는 함수
                return ("text", f"[오류] spec.json 읽기 실패: {e}")

        if os.path.exists(spec_txt): #만약 spec_txt의 경로로 읽고 싶다면
            try:
                with open(spec_txt, "r", encoding="utf-8") as f:
                    txt = f.read()
                if not txt.strip():
                    return ("text", "[안내] spec.txt가 비어 있습니다. 내용을 넣어주세요.\n")
                    # spec_txt 파일을 읽기모드(r)로 연다
                    # enconding utf-8을 지정해서 한글도 읽을 수 있게 한다
                    # with as f문을 사용하면 블록이 끝날 때 파일이 자동으로 닫힌다
                    return ("text", f.read()) #text 반환
                return ("text", txt)
            except Exception as e: # 예외가 일어날 시 오류 문구를 나타내는 함수
                return ("text", f"[오류] spec.txt 읽기 실패: {e}")
            
        txt_files = [fn for fn in os.listdir(model_path) if fn.lower().endswith(".txt")]
        if txt_files:
            txt_files.sort(key=lambda x: (x != "제원.txt", x))
            chosen = os.path.join(model_path, txt_files[0])
            try:
                with open(chosen, "r", encoding="utf-8") as f:
                    txt = f.read()
                if not txt.strip():
                    return ("text", f"[안내] {txt_files[0]}가 비어 있습니다. 내용을 넣어주세요.\n")
                return ("text", txt)
            except Exception as e:
                return ("text", f"[오류] {txt_files[0]} 읽기 실패: {e}")

        return ("text", "[안내] 제원 파일(spec.json/spec.txt)이 없습니다.\n")

    def find_images(self, model_path): #모델 이미지를 찾는 함수
        img_dir = os.path.join(model_path, "images") # model_path를 통해서 images 폴더 경로 찾아서 저장 => img_dr
        base = img_dir if os.path.isdir(img_dir) else model_path
        
        imgs = [] # 이미지를 넣을 수 있는 빈 리스트 만들기
        for fn in os.listdir(base): # base : 어느 폴더를 탐색할지 결정된 폴더 경로
            if fn.lower().endswith((".png", ".gif")):
                imgs.append(os.path.join(base, fn))
        # png, gif 골라내는 루프
        return sorted(imgs) #정렬

    # ----------------------------
    # 리스트/상세 로직
    # ----------------------------
    def load_models(self, fuel): # 차종 목록을 listbox에 표시하는 함수
        self.models_listbox.delete(0, END)
        #models_listbox를 0부터 끝까지 지운다 -> 기존에 남아있던 기록들 삭제
        #연료를 바꿀 때 이전기록이 남지 않게 하기 위함

        folders, fuel_path = self.list_models(fuel)
        #연료별 list_models들을 folders(차종 폴더 목록), fuel_path(연료 폴더 경로) 경로를 가져온다
        
        if folders is None: #만약 folders 폴더가 아무것도 없다면?
            self.models_listbox.insert(END, f"[오류] 폴더 없음: {fuel_path}") #listbox에 폴더 없음을 삽입
            return #반환

        if not folders: #그게 아니라면(내용이 비어 있다면)
            self.models_listbox.insert(END, "[안내] 차종 폴더가 없습니다.") #"차종 폴더가 없습니다"를 listbox에 삽입
            return #반환

        for name in folders: 
            self.models_listbox.insert(END, name) #folders안에 있는 폴더들을 끝에서부터 한개씩 listbox에 삽입

    def open_detail(self, event=None):
        #리스트에서 선택한 차종을 기준으로 상세 화면을 열기 위해 필요한 정보를 준비하고 load_detail()을 호출하는 ‘연결 함수'
        sel = self.models_listbox.curselection() #curselection() -> 튜플로 반환
        #리스트 박스에서 선택된 것을 튜플로 반환하여 저장 -> sel
        if not sel: #선택이 없다면
            return #그냥 반환
        model_name = self.models_listbox.get(sel[0]) # models_listbox에서 0번째 인덱스에 선택된 것을 가져와서 저장 => model name
        fuel = self.fuel_var.get() # fuel_var에서 가져온 정보를 fuel에 저장
        self.load_detail(fuel, model_name) #상세 페이지에 연료와 모델 이름 전달할 수 있게 준비

    def load_detail(self, fuel, model_name): # 이미 전달받은 연료와 차량 이름을 상세 페이지에 업로드 하는 함수
        model_path = self.model_dir(fuel, model_name) # 연료와 차량 이름을 조합해서 차종 폴더의 경로를 가져온다 => model_path

        self.detail_title.configure(text=f"{model_name} 상세") # 상세 페이지 title을 {model_name} 상세로 바꾼다.
        self.detail_spec.delete("1.0", END) # 다음 목록을 보기 위해 차량의 상세 내용의 이전 기록을 지운다
        # 1.0은 처음 이라는 뜻 => 즉 처음 부터 end(끝까지)

        if not os.path.isdir(model_path): # 만약 model_path의 경로를 검사해서 없다면?
            self.detail_spec.insert(END, f"[오류] 차종 폴더가 없습니다.\n{model_path}\n")
            # detail_spec에 끝에서부터 [오류] 차종 폴더가 없습니다.\n{model_path}\n 삽입
            self.detail_images = [] # model_path가 없으니깐 이미지가 없다는 것을 명시적으로 알리
            self.show_detail_image(0) # model_path가 없으면 인덱스 0번째 부터 상세페이지에 이미지가 없다는 것을 보여준다.
            self.show_frame(self.detail_frame) # 상세 페이지 프레임을 보여준다.
            return #오류 처리 함수 종료

        # 제원 표시
        kind, spec_data = self.read_spec(model_path) # 튜플의 언패킹 -> 두개의 값을 동시에 반환
        # model_path 경로를 통해 온 spec를 읽어 kind와 spec_data의 두개 값을 동시에 반환
        if kind == "json" and isinstance(spec_data, dict):
            # read 함수가 “read_spec()이 JSON 형식으로 읽었고, 그 결과가 딕셔너리일 경우”
            for k, v in spec_data.items():
                self.detail_spec.insert(END, f"{k}: {v}\n")
            # spec_data의 요소들을 k : v로 하나씩 삽입하기
            
        else: #그게 아니라면
            self.detail_spec.insert(END, str(spec_data)) #다른 형식의 spec_data로 읽어다면 그 형식에 맞게 삽입
        # 저는 제원파일이 txt만 써서 굳이 spec.json이 필요하지 않지만 확장성을 위해 코딩

        # 이미지 표시
        self.detail_images = self.find_images(model_path)
        # 차종 폴더(model_path)에서 이미지 파일(.png, .gif)을 찾아
        # 이미지 파일 경로 목록을 detail_images에 저장한다
        self.detail_img_idx = 0
        # 새 차종을 선택했으므로
        # 현재 이미지 인덱스를 0(첫 번째 이미지)으로 초기화한다
        self.show_detail_image(0) # 0번째 이미지부터 사용자에게 보여준다.

        self.show_frame(self.detail_frame)
        # container에 겹쳐진 화면들 중에서
        # 상세 정보 화면(detail_frame)을 맨 위로 올려 사용자에게 표시한다

    def _fit_photoimage(self, img_path, max_w=550, max_h=400): # 이미지 파일 경로를 읽어와서 크기 맞추는 함수
        """PhotoImage를 subsample로 대충 맞추기(정수 축소만 가능)"""
        img = PhotoImage(file=img_path) # img_path 경로로 부터 이미지를 객체화 시켜 저장 => img
        w, h = img.width(), img.height() #가로 세로 크기 정의

        scale = max(w / max_w, h / max_h) #가로 기준 비율, 세로 기준 비율 둘 중 더 큰 값을 선택하여 scale에 저장
        if scale > 1: # scale이 1보다 크다면 -> 이미지가 너무 크다는 뜻 -> 축소 필요
            factor = int(scale) + 1 # scale에다가 1을 더해 factor에 저장 -> subsample 1/n으로 축소하기 때문에 분모가 커져야지 이미지가 축소
            img = img.subsample(factor, factor) # 가로 세로 동일한 비율로 맞추기 
        return img #변형된 이미지 반환 

    def show_detail_image(self, idx): # 상세 페이지 이미지 존재 여부를 보여주는 함수
        if not self.detail_images: #만약 상세 페이지 이미지가 저장이 안되어있다면?
            self.detail_img_label.configure(image="", text="[안내] 이미지가 없습니다.", compound="center")
            # 상세 페이지 이미지 란에 이미지는 없고 "[안내] 이미지가 없습니다." 문구를 중앙에 배치
            return # 함수 실행 후 종료

        self.detail_img_idx = idx % len(self.detail_images) # 어떠한 화면에서 순환시킬 수 있는  순환 코드
        # 전달받은 idx 값을 이미지 개수로 나눈 나머지로 현재 이미지 인덱스를 결정
        # → 이전/다음 버튼을 눌러도 인덱스가 범위를 벗어나지 않게 하기 위함
        # → 음수나 초과 값도 자연스럽게 순환(loop)되도록 만든 처리
        # for문과 if문으로도 구현은 가능하지만,% 연산자는 이 문제를 위해 존재하는 수준의 최적해.
        
        img_path = self.detail_images[self.detail_img_idx]
        # 상세이미지의 현재 인덱스에 해당하는 이미지 파일 경로를 가져온다 => img_path

        try: # 이미지 로딩과 표시 과정은 실패할 가능성이 있기 때문에 프로그램이 죽지 않도록 보호하는 영역
            self.detail_photo = self._fit_photoimage(img_path)
            # 이미지 파일 경로(img_path)를 이용해
            # 상세 페이지 레이아웃에 맞게 크기를 조정한 PhotoImage 생성
            self.detail_img_label.configure(image=self.detail_photo, text="")
            # Label에 이미지 적용
            # text="" → 이전 오류/안내 텍스트가 있다면 제거
        except Exception as e: # try 블록 안에서 어떤 종류의 오류라도 발생하면 이쪽으로 이동
            self.detail_img_label.configure(image="", text=f"[오류] 이미지 표시 실패\n{e}", compound="center")
            # 이미지 로딩 또는 표시 중 오류가 발생한 경우
            # 앱이 종료되지 않도록 이미지 대신 오류 메시지를 표시
            
    def change_image(self, delta): # 상세 페이지 순환 코드 함수
        # delta 값만큼 현재 이미지 인덱스를 이동시킨다
        # (예: +1 = 다음, -1 = 이전)
        if not self.detail_images: # 만약 상세 이미지가 없다면
            return #함수 종료
        self.show_detail_image(self.detail_img_idx + delta)
        # 현재 이미지 인덱스에 delta를 더한 값을 전달하여
        # 실제 이미지 표시 및 인덱스 보정은 show_detail_image()에 맡긴다
        
    # ----------------------------
    # 실행
    # ----------------------------
    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = HyundaiCarDictionary()
    app.run()
