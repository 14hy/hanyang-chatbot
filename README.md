# Hanyang-Univ Erica Campus Chatbot


| ![image](https://user-images.githubusercontent.com/12870549/67618253-e15ea500-f827-11e9-9b4a-a79352ecd916.png) | ![image](https://user-images.githubusercontent.com/12870549/67618289-5336ee80-f828-11e9-9cd3-6cfc7978efd2.png) | ![image](https://user-images.githubusercontent.com/12870549/67618193-10c0e200-f827-11e9-92f4-5d2f4a27b44f.png) |
|----------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------|



### Pre-requisites

- [Node.js][nodejs-url] >= `10.18.1`
- [NPM][npm-url] >= `6.13.4`
- [JDK](https://www.oracle.com/java/technologies/javase-jdk8-downloads.html) >= 8
- Gradle - 없다면 [이 사이트](https://zetawiki.com/wiki/%EC%9C%88%EB%8F%84%EC%9A%B0_gradle_%EC%84%A4%EC%B9%98) 참고해서 받을 것
- (Android) Android SDK - 없다면 [이 사이트](https://developer.android.com/studio/install?hl=ko) 참고해서 받을 것
- (IOS) xcode >= lateset

#### 환경변수 설정

- SDK 폴더 내, `tools`, `platform-tools` 폴더 2개를 시스템 환경변수에 추가
- `Gradle` 폴더 추가

### Install

```sh
# /client 경로에서 칠 것!

npm install

npm install -g cordova

cordova prepare
```

### Serve

```sh
# 브라우저에서 테스트
# mode: development
npm run dev
# mode: production - production 상태(deploy 버전)
npm run production

# 안드로이드 기기에서 테스트 (연결된 기기 없으면 예물레이터가 켜짐)
# npm run production 명령어 이후에 할 것! (빌드된 파일이 존재해야함)
npm run android

# IOS 기기에서 테스트
cordova build ios
# 이후, /client/platforms/ios/하냥봇.xcwork 가 추가되며 Login 관련으로 로그인 build 가 실패할 시
# 가지고 있는 계정으로 위 파일에서 직접 등록해놓고 다시 build 해야 합니다.
```

### Build (for. production)
```sh
cordova build android --release

# 이후 /client/platforms/android/app/build/outputs/apk/release 경로에 app-release-unsigned.apk 파일이 생성됨

# 이 파일을 가지고 hanyang.keystore을 이용해 암호화 - 암호화 파일(현재 '강태욱'이 소유 중)
# hanyang.keystore와 apk파일을 같은 경로에 넣고 명령어 치면 됨
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore hanyang.keystore app-release-unsigned.apk android-app-key

zipalign -v 4 app-release-unsigned.apk app-release.apk

# 이후, 구글 개발자 콘솔에 가서 해당 apk를 배포
```



### 진행 스샷

```sh
npm install

# 스크린샷 생략
```

```sh
npm i -g cordova
```

![image-20200405231117899](https://raw.githubusercontent.com/taeuk-gang/save-image-repo/image/img/image-20200405231117899.png)

```sh
cordova prepare

# Window 환경은 아래와 같이 IOS(xcode)가 없어서 Fail 뜨게됨
```

![image-20200405231218853](https://raw.githubusercontent.com/taeuk-gang/save-image-repo/image/img/image-20200405231218853.png)

```sh
npm run production
```

![image-20200405231359294](https://raw.githubusercontent.com/taeuk-gang/save-image-repo/image/img/image-20200405231359294.png)

```sh
cordova run android

# android sdk가 없다면 첫번째 그림과 같은 에러가 뜬다
# 성공시 2번째 그림처럼 되고, 기기에서 실행됨
```

![image-20200405231629537](https://raw.githubusercontent.com/taeuk-gang/save-image-repo/image/img/image-20200405231629537.png)

![image-20200405235929490](https://raw.githubusercontent.com/taeuk-gang/save-image-repo/image/img/image-20200405235929490.png)

### 기타

기타 자세한 설명은 [이 사이트](https://cordova.apache.org/docs/ko/latest/guide/cli/index.html)를 참고할 것
