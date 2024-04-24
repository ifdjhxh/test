using namespace std;

struct NewStruct{
};

class MyClass {
protected:
    MyClass(){
        cout << 'hello' << endl;
    }
    int a = 10;
    void member_function(int arg1, float arg2) {}
    ~MyClass(){
        cout << 'уничтожился' << endl;
    }
};

int main() {
    int local_variable;
    int a = 10, b = 5;
    if (a > b){
        std::cout << a;
    }
    for (int i; i<10; i++){
        i++;
    }
    MyClass obj;
    obj.member_function(1, 3.14);
    return 0;
}
