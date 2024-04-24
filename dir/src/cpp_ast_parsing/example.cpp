using namespace std;

struct NewStruct{
};

class MyClass {
protected:
    MyClass(){
        cout << 'hello' << endl;
    }
    char a = "a";
    void member_function(int arg1, float arg2) {}
    ~MyClass(){
        cout << 'уничтожился' << endl;
    }
};

int main() {
    int local_variable;
    int b = 10;
    MyClass obj;
    obj.member_function(1, 3.14);
    return 0;
}