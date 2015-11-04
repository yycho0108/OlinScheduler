#define _CRT_SECURE_NO_WARNINGS
#include <Windows.h>
#include <stdio.h>
#include <vector>
#include <fstream>
#include <iostream>
#include <string>

HINSTANCE g_hInst;
HWND hMainWnd;
LPTSTR title = TEXT("OlinScheduler");
HRESULT CALLBACK WndProc(HWND hWnd, UINT uMsg, WPARAM wParam, LPARAM lParam);
using namespace std;
struct Class {

	string area, ID;
	int sectionNumber;
	string title, instructor;
	vector<int> time;
	string location;
	int credits;
	int enrollLimit;
	string notes;

	Class(std::vector<std::string>& vCat) {
		area = vCat[0];
		ID = vCat[1];
		sscanf(vCat[2].c_str(), "%d", &sectionNumber);
		title = vCat[3];
		instructor = vCat[4];
		time = { 0,0 }; //FOR NOW
		location = vCat[6];
		sscanf(vCat[7].c_str(), "%d", &credits);
		sscanf(vCat[8].c_str(), "%d", &enrollLimit);
		notes = vCat[9];
	}
	std::wstring toW(std::string& str) { return std::wstring(str.begin(), str.end()); }
	std::wstring toW(int num) { return std::to_wstring(num); }
	void display(HDC hdc,int x,int y) {
		std::wstring msg = toW(area) + toW(ID)+ toW(sectionNumber) + toW(title) + toW(instructor) //<< time
			+ toW(location) + toW(credits) + toW(enrollLimit) + toW(notes);
		TextOut(hdc, x, y, msg.c_str(), msg.length());
	}
};
vector<Class> cList;

ATOM RegisterCustomClass(HINSTANCE hInst) {
	WNDCLASS w;
	w.cbClsExtra = 0;
	w.cbWndExtra = 0;
	w.hbrBackground = GetSysColorBrush(COLOR_WINDOW);
	w.hCursor = LoadCursor(NULL, IDC_ARROW);
	w.hIcon = LoadIcon(NULL, IDI_APPLICATION);
	w.hInstance = hInst;
	w.lpfnWndProc = WndProc;
	w.lpszClassName = title;
	w.lpszMenuName = NULL;
	w.style = CS_VREDRAW | CS_HREDRAW;
	return RegisterClass(&w);
}
int APIENTRY WinMain(HINSTANCE hInst, HINSTANCE, LPSTR, int nCmdShow) {
	g_hInst = hInst;
	RegisterCustomClass(hInst);
	hMainWnd = CreateWindow(title, title, WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT, NULL, NULL, hInst, NULL);
	ShowWindow(hMainWnd, nCmdShow);

	MSG msg;
	while (GetMessage(&msg, NULL, NULL, NULL)) {
		TranslateMessage(&msg);
		DispatchMessage(&msg);
	}
	return msg.wParam;
}

inline bool checkDelim(char b, std::vector<char>& delim) {
	for (auto d : delim) {
		if (b == d)
			return true;
	}
	return false;
}
std::vector<std::string> split(std::string& src, char* d) {
	std::string s(d);
	std::vector<char> delim(s.begin(), s.end());
	
	std::vector<std::string> dst({""});
	int index = 0;
	for (auto c : src) {
		if (checkDelim(c, delim))
			dst.push_back(std::string(""));
		else
			dst.back().push_back(c);
	}
	return dst;
}
enum{AREA,ID,SECTION,TITLE,INSTRUCTOR,TIME,LOCATION,CREDITS,LIMITS,NOTES};
void ParseData()
{
	std::ifstream f_in("Data.csv");
	std::string str;
	while (std::getline(f_in, str)) {
		auto categories = split(str, ",");
		cList.push_back(Class(categories));
	}
	f_in.close();
}
void visualize(vector<Class>& cList) {

}
HRESULT CALLBACK WndProc(HWND hWnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
	switch (uMsg) {
	case WM_CREATE:
		ParseData();
		hMainWnd = hWnd;
		break;
	case WM_PAINT:
	{
		PAINTSTRUCT ps;
		int x = 0, y = 0;
		HDC hdc = BeginPaint(hWnd, &ps);
		for (auto c : cList) {
			c.display(hdc, x, y += 50);
		}
		EndPaint(hWnd, &ps);
		break;
	}
	case WM_DESTROY:
		PostQuitMessage(0);
		break;
	default:
		return DefWindowProc(hWnd, uMsg, wParam, lParam);
	}
	return 0;
}