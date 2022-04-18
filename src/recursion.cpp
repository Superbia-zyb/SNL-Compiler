#include <bits/stdc++.h>
using namespace std;
extern "C"{
	//enum SNL_TYPE {Reserved_Word,Other,ID,INTC,CHARC,EOF} ;//五大类型
static int line;//行号
static string type;//类型
static string token;//具体标识
static ifstream input;//输入流
static ofstream output;//输出流
static bool has_unread=false;
static string temp_name;
typedef enum {ProK,PheadK,TypeK,VarK,ProcDecK,StmLK,DecK,StmtK,ExpK}NodeKind;
typedef enum {ArrayK,CharK,IntegerK,RecordK,IdK}  DecKind;
typedef enum {IfK,WhileK,AssignK,ReadK,WriteK,CallK,ReturnK} StmtKind;
typedef enum {OpK,ConstK,VariK} ExpKind;//表达式类型分为操作符类型：a+b 常整数类型：6 变量类型：a
typedef enum {IdV,ArrayMembV,FieldMembV} VarKind; //标识符变量 数组成员变量 域成员变量
typedef enum {Void,Integer,Boolean} ExpType;//表达式整个节点的检查类型（为语义分析判别打基础
typedef enum {none,varparamType,valparamType} ParamType;
typedef struct Node
{
	bool work;
	struct Node * child[3];		/* 子节点指针	*/
    struct Node * sibling;					/* 兄弟节点指针	*/
    int lineno;								/* 源代码行号	*/
    NodeKind nodekind;						    /* 节点类型		*/
    union
	{
		DecKind  dec;
	    StmtKind stmt;
		ExpKind  exp;
	} kind;                       /* 具体类型     */

	int idnum;                    /* 相同类型的变量个数 */

	//char name[10][10];            /* 标识符的名称  */
	string name[10];			/* 标识符的名称  */
	//struct symbtable * table[10]; /* 与标志符对应的符号表地址，在语义分析阶段填入*/

	struct
	{
		struct
			{
				int low;              /* 数组下界     */
				int up;               /* 数组上界     */
				DecKind   childtype;  /* 数组的子类型 */
			}ArrayAttr;               /* 数组属性     */

		struct
			{
				ParamType  paramt;     /* 过程的参数类型*/
			}ProcAttr;                 /* 过程属性      */

		struct
			{
				string op;           /* 表达式的操作符*/		//< =
				int val;		      /* 表达式的值	   */
				VarKind  varkind;     /* 变量的类别    */
				ExpType type;         /* 用于类型检查  */
			}ExpAttr;	              /* 表达式属性    */

    //char type_name[10];             /* 类型名是标识符  */   type a=integer; var a x;中的x节点，其中type_name记录a
    	string type_name;             /* 类型名是标识符  */ //记录类型名,当节点为声明类型,且类型是由类型标志符表示时有效。

	} attr;                          /* 属性	       */
}Node;

Node* parse();
Node* program();
Node * program_head();
Node *declare_part();

Node *TypeDec();
Node *TypeDeclaration();
Node *TypeDecList();
void TypeId(Node *t);
void TypeName(Node *t);
void BaseType(Node *t);
void StructureType(Node *t);
void ArrayType(Node *t);
void RecType(Node *t);
Node *FieldDecList();
Node *FieldDecMore();
void IdList(Node *t);
void IdMore(Node *t);
Node *TypeDecMore();

Node *VarDec();
Node *VarDeclartion();
Node *VarDecList();
void VarIdList(Node *t);
void VarIdMore(Node *t);
Node*VarDecMore();

Node *ProcBody();
Node *ProcDecPart();
Node *ParamMore();
void FidMore(Node *t);
void FormList(Node *t);
Node *Param();
Node *ParamDecList();
void ParamList(Node *t);
Node *ProcDeclaration();
Node *ProcDec();

Node *factor();
Node *term();
Node *simple_exp();
Node *Exp();
void variMore(Node *t);
Node *variable();
void fieldvarMore(Node *t);
Node *fieldvar();
Node *AssignmentRest();
Node *ActParamMore();
Node *ActParamList();
Node *CallStmRest();
Node *AssCall();
Node *ReturnStm();
Node *OutputStm();
Node *InputStm();
Node *LoopStm();
Node *ConditionalStm();
Node *Stm();
Node *StmMore();
Node *StmList();
Node *program_body();

void read_token();
void error(int ll,string s);
void print_null(int n);
void print_tree(Node *t,int n);
void match(string s);
Node *init_node();

void read_token(){
	input>>line>>type>>token;
	//output<<line<<" "<<type<<" "<<token<<endl;
	//要加类型，行号，具体表达串
}
void error(int ll,string s){
	output<<"line:"<<ll<<" "<<s<<endl;
}
void print_null(int n){
	while(n--!=0) output<<"   ";
}
void print_tree(Node *t,int n){
while(t!=NULL){
	if((t->nodekind==TypeK||t->nodekind==VarK||t->nodekind==ProcDecK||t->nodekind==StmLK)&&(t->child[0]==NULL)) {
		t=t->sibling;
		continue;
	}
	print_null(n);
	if(t->nodekind==ProK) {
		output<<"ProK "<<t->lineno<<endl;
	}
	else if(t->nodekind==PheadK){
		output<<"PheadK "<<t->lineno<<" "<<t->name[0]<<endl;
	}
	else if(t->nodekind==TypeK){
		output<<"TypeK "<<t->lineno<<endl;
	}
	else if(t->nodekind==VarK){
		output<<"VarK "<<t->lineno<<endl;
	}
	else if(t->nodekind==ProcDecK){
		output<<"ProcDecK "<<t->lineno<<" "<<t->name[0]<<endl;
	}
	else if(t->nodekind==StmLK){
		output<<"StmLK "<<t->lineno<<endl;
	}
	else if(t->nodekind==DecK){
		output<<"DecK "<<t->lineno<<" ";
		if(t->attr.ProcAttr.paramt==varparamType) output<<"varparamType ";
		else if(t->attr.ProcAttr.paramt==valparamType) output<<"valparamType ";
		if(t->kind.dec==ArrayK){
			string ss;
			if(t->attr.ArrayAttr.childtype==0) ss="ArrayK";
			else if(t->attr.ArrayAttr.childtype==1) ss="CharK";
			else if(t->attr.ArrayAttr.childtype==2) ss="IntegerK";
			else if(t->attr.ArrayAttr.childtype==3) ss="RecordK";
			else if(t->attr.ArrayAttr.childtype==4) ss="IdK";
			output<<"ArrayK "<<t->attr.ArrayAttr.low<<" "<<t->attr.ArrayAttr.up<<" "<<ss<<" ";
			for(int i=0;i<t->idnum;i++)
				output<<t->name[i]<<" ";
			output<<endl;
		}
		else if(t->kind.dec==CharK){
			output<<"CharK ";
			for(int i=0;i<t->idnum;i++)
				output<<t->name[i]<<" ";
			output<<endl;
		}
		else if(t->kind.dec==IntegerK){
			output<<"IntegerK ";
			for(int i=0;i<t->idnum;i++)
				output<<t->name[i]<<" ";
			output<<endl;
		}
		else if(t->kind.dec==RecordK){
			output<<"RecordK ";
			for(int i=0;i<t->idnum;i++)
				output<<t->name[i]<<" ";
			output<<endl;
			//for(int i=0;i<3;i++) if(t->child[i]!=NULL) print_tree(t->child[i],n+1);
		}
		else if(t->kind.dec==IdK){
			output<<"IdK ";
			for(int i=0;i<t->idnum;i++)
				output<<t->name[i]<<" ";
			output<<endl;
		}
		else {
			error(t->lineno,"there is no correct decKindName");
		}
	}
	else if(t->nodekind==StmtK){
		output<<"StmtK "<<t->lineno<<" ";
		if(t->kind.stmt==IfK){
			output<<"IfK "<<endl;
			//for(int i=0;i<3;i++) if(t->child[i]!=NULL) print_tree(t->child[i],n+1);
		}
		else if(t->kind.stmt==WhileK){
			output<<"WhileK "<<endl;
			//for(int i=0;i<3;i++) if(t->child[i]!=NULL) print_tree(t->child[i],n+1);
		}
		else if(t->kind.stmt==AssignK){
			output<<"AssignK "<<endl;
			//for(int i=0;i<3;i++) if(t->child[i]!=NULL) print_tree(t->child[i],n+1);
		}
		else if(t->kind.stmt==ReadK){
			output<<"ReadK "<<t->name[0]<<endl;
		}
		else if(t->kind.stmt==WriteK){
			output<<"WriteK "<<endl;
			//for(int i=0;i<3;i++) if(t->child[i]!=NULL) print_tree(t->child[i],n+1);
		}
		else if(t->kind.stmt==CallK){
			output<<"CallK "<<t->name[0]<<endl;
			//for(int i=0;i<3;i++) if(t->child[i]!=NULL) print_tree(t->child[i],n+1);
		}
		else if(t->kind.stmt==ReturnK){
			output<<"ReturnK "<<endl;
			//for(int i=0;i<3;i++) if(t->child[i]!=NULL) print_tree(t->child[i],n+1);
		}
		else {
			error(t->lineno,"there is no correct stmtKindName");
		}
	}
	else if(t->nodekind==ExpK){
		output<<"ExpK "<<t->lineno<<" ";
		if(t->kind.exp==OpK){
			output<<"OpK "<<t->attr.ExpAttr.op<<endl;
			//for(int i=0;i<3;i++) if(t->child[i]!=NULL) print_tree(t->child[i],n+1);
		}
		else if(t->kind.exp==ConstK){
			output<<"ConstK"<<" "<<t->attr.ExpAttr.val<<endl;
		}
		else if(t->kind.exp==VariK){
			string ss;
			VarKind s=t->attr.ExpAttr.varkind;
			if(s==0) ss="IdV";
			else if(s==1) ss="ArrayMembV";
			else ss="FieldMembV";
			output<<"IdK "<<ss<<" "<<t->name[0]<<endl;
//			s=={IdV,ArrayMembV,FieldMembV} VarKind s;
//			s==
		}
	}
	else {
		error(t->lineno,"the nodekind is not correct");
	}
	for(int i=0;i<3;i++) if(t->child[i]!=NULL) print_tree(t->child[i],n+1);//打印儿子节点
	t=t->sibling;//打印兄弟节点
}
}
void match(string s){
	if(token!=s) output<<"line:"<<line<<" there misses "<<s<<" to match"<<endl;
	//read_token();
}
Node *init_node(){
	Node *t=new(Node);
	t->attr.ProcAttr.paramt=none;
	t->work=true;
	t->idnum=0;
	for(int i=0;i<3;i++) t->child[i]=NULL;
	t->sibling = NULL;
	t->lineno = line;
	return t;
}

/////////////////////////////////program_body部分

Node *factor(){
	//output<<"factor"<<endl;
	if(type=="INTC"){
		Node *t=init_node();t->nodekind=ExpK;t->kind.exp=ConstK;t->attr.ExpAttr.val=atoi(token.c_str());
		read_token();return t;
	}
	else if(type=="ID"){
		return variable();
	}
	else if(token=="("){
		//output<<"====================="<<token<<endl;
		read_token();
		Node *t= Exp();
		if(token!=")")error(line,"there is no ) to match");

		read_token();
		return t;
	}
	else {
		error(line,"there is no ( ID INTC to match");
		read_token();
		return NULL;
	}
}
Node *term(){
	//output<<"term"<<endl;
	Node *t=factor();
	//read_token();
	while(token=="*"||token=="/"){
		Node *p=init_node();p->nodekind=ExpK;p->kind.exp=OpK;
		p->child[0]=t;p->attr.ExpAttr.op=token;
		t=p;
		read_token();
		t->child[1]=factor();//要不要read看factor读完以后
	}
	return t;
}
Node *simple_exp(){
	//output<<"simple_exp"<<endl;
	Node *t=term();
	//read_token();
	while(token=="+"||token=="-"){
		Node *p=init_node();p->nodekind=ExpK;p->kind.exp=OpK;
		p->child[0]=t;p->attr.ExpAttr.op=token;
		t=p;
		read_token();
		t->child[1]=term();//要不要read看term读完以后
	}
	return t;
}
Node *Exp(){//v1-(10-11)
	//output<<"Exp"<<endl;
	Node *t=simple_exp();
	//read_token();
	if(token=="<"||token=="="){
		Node *p=init_node();p->nodekind=ExpK;p->kind.exp=OpK;p->attr.ExpAttr.op=token;
		p->child[0]=t;
		t=p;
		read_token();
		if(t!=NULL) t->child[1]=simple_exp();
		return t;
	}
	else return t;
}
void variMore(Node *t){
	//output<<"variMore"<<endl;
//	output<<token<<endl;
//	output<<has_unread<<endl;
	//if(has_unread==false) read_token();has_unread=false;
	vector<string> s={"+", "ELSE", "=", "DO", "FI", "<", "]", ";", "*", ")", "ENDWH", "-", ",", "END", "/", ":=", "THEN"};
//	output<<token<<endl;
	if(find(s.begin(),s.end(),token)!=s.end()){
		//output<<"has return"<<endl;
		t->attr.ExpAttr.varkind=IdV;
		return ;
	}
	else if(token=="["){
		t->attr.ExpAttr.varkind=ArrayMembV;
		read_token();t->child[0]=Exp();t->child[0]->attr.ExpAttr.varkind = IdV;//中括号内是标识符变量
		if(token!="]") error(line,"there is no ] to match");
		read_token();//书上没有

	}
	else if(token=="."){
		t->attr.ExpAttr.varkind=FieldMembV;
		read_token();t->child[0]=fieldvar();t->child[0]->attr.ExpAttr.varkind = IdV;
	}
	else {
		error(line,"there is no . [ to match");
		read_token();
	}
}
Node *variable(){
	//output<<"variable"<<endl;
	Node *t=init_node();t->nodekind=ExpK;t->kind.exp=VariK;t->name[t->idnum++]=token;
//	if(type=="ID") {
//
//	}
	read_token();
	variMore(t);
	return t;
}
void fieldvarMore(Node *t){
	//output<<"fieldvarMore"<<endl;
	vector<string> s={"+", "ELSE", "=", "DO", "FI", "<", "]", ";", "*", ")", "ENDWH", "-", ",", "END", "/", ":=", "THEN"};
	//read_token();
	if(find(s.begin(),s.end(),token)!=s.end()){
		return ;
	}
	else if(token=="["){
		read_token();
		t->child[0]=Exp();
		t->child[0]->attr.ExpAttr.varkind=ArrayMembV;
		if(token!="]") error(line,"there is no ] to match");
		read_token();
	}
	else {
		error(line,"there is no correct to match");
		read_token();
	}
}
Node *fieldvar(){
	//output<<"fieldvar"<<endl;
	Node *t=init_node();
	if(type=="ID"){
		t->nodekind=ExpK;t->kind.exp=VariK;t->name[t->idnum++]=token;

	}
	else error(line,"there is no ID to match");
	read_token();
	fieldvarMore(t);
	return t;
}
Node *AssignmentRest(){//v1-(10-11)
	//output<<"AssignmentRest"<<endl;
	Node *t=init_node();t->nodekind=StmtK;t->kind.stmt=AssignK;
	Node *p=init_node();p->nodekind=ExpK;p->kind.exp=VariK;p->name[p->idnum++]=temp_name;
	variMore(p);t->child[0]=p;//进入的时候token已经有[ := .了
	//if(has_unread==false) read_token();has_unread=false;//默认要读，除非has_unread=true
	if(token!=":=") error(line,"there is no := to match");
	read_token();
	t->child[1]=Exp();//v1+10
	return t;
}
Node *ActParamMore(){
	//output<<"ActParamMore"<<endl;
	if(token==",") {
		read_token();
		return ActParamList();
	}
	else if(token==")") return NULL;
	else {

		error(line,"there is no ) or , to match");
		read_token();
		return NULL;
	}
}
Node *ActParamList(){
	//output<<"ActParamList"<<endl;

	if(token==")"){
		return NULL;
	}
	else if(token=="("||type=="ID"||type=="INTC"||type=="CHARC"){
		Node *t=Exp();
		t->sibling=ActParamMore();
		return t;
	}
	else {
		error(line,"there is no ) or ID INTC CHARC to match");
		read_token();
		return NULL;
	}
}
Node *CallStmRest(){
	//output<<"CallStmRest"<<endl;
	Node *t=init_node();t->nodekind=StmtK;t->kind.stmt=CallK;t->name[t->idnum++]=temp_name;
	if(token!="(") error(line,"there is no ( to match");
	read_token();t->child[0]=ActParamList();
	if(token!=")") error(line,"there is no ) to match");
	read_token();
	return t;
}
Node *AssCall(){//else 后面的部分
	//output<<"AssCall"<<endl;
	//read_token();
	if(token=="(") {return CallStmRest();
	}
	else if(token=="["||token==":="||token==".") return AssignmentRest();
	else {
		error(line,"there is no [ := . ( to match");
		read_token();
		return NULL;
	}
}
Node *ReturnStm(){//退出时是； （和书上不一样）
	//output<<"ReturnStm"<<endl;
	Node *t=init_node();t->nodekind=StmtK;t->kind.stmt=ReturnK;
	if(token!="RETURN") error(line,"there is no RETURN to match");
	read_token();
	if(token!="("){error(line,"there is no ( to match");}
	read_token();

	t->child[0]=Exp();
	if(token!=")") error(line,"there is no ) to match");
	read_token();
	return t;
}
Node *OutputStm(){//退出时是；
	//output<<"OutputStm"<<endl;
	Node *t=init_node();t->nodekind=StmtK;t->kind.stmt=WriteK;
	if(token!="WRITE") error(line,"there is no WRITE to match");
	read_token();
	if(token!="("){error(line,"there is no ( to match");}
	read_token();

	t->child[0]=Exp();
	if(token!=")") error(line,"there is no ) to match");
	read_token();
	return t;
}
Node *InputStm(){//退出时是；
	//output<<"InputStm"<<endl;
	Node *t=init_node();t->nodekind=StmtK;t->kind.stmt=ReadK;
	if(token!="READ") error(line,"there is no READ to match");
	read_token();
	if(token!="("){error(line,"there is no ( to match");}
	read_token();

	if(type=="ID"){
		t->name[t->idnum++]=token;
	}
	else error(line,"there is no ID to match");

	read_token();
	if(token!=")") error(line,"there is no ) to match");
	read_token();
	return t;
}
Node *LoopStm(){//退出时是endwh下一个 (和书上不一样)
	//output<<"LoopStm"<<endl;
	Node *t=init_node();t->nodekind=StmtK;t->kind.stmt=WhileK;
	if(token!="WHILE") error(line,"there is no WHILE to match");
	read_token();t->child[0]=Exp();
	if(token!="DO") {error(line,"there is no DO to match");}
	read_token();t->child[1]=StmList();
	if(token!="ENDWH") {error(line,"there is no ENDWH to match");}
	read_token();
	return t;
}
Node *ConditionalStm(){//退出时是FI下一个
	//output<<"ConditionalStm"<<endl;
	Node *t=init_node();t->nodekind=StmtK;t->kind.stmt=IfK;
	if(token!="IF") error(line,"there is no IF to match");
	read_token();
	t->child[0]=Exp();

	if(token!="THEN"){error(line,"there is no THEN to match");};
	read_token();
	t->child[1]=StmList();//条件为真的语句

	if(token=="ELSE"){
		read_token();t->child[2]=StmList();//条件为假的语句
	}

	if(token!="FI"){error(line,"there is no FI to match");};
	read_token();

	return t;
}
Node *Stm(){//AssCall前面比书多读了
	//output<<"Stm"<<endl;
	if(token=="IF"){return ConditionalStm();}
	else if(token=="WHILE") return LoopStm();
	else if(token=="READ") return InputStm();
	else if(token=="WRITE") return OutputStm();
	else if(token=="RETURN") return ReturnStm();
	else if(type=="ID") {temp_name=token;read_token();return AssCall();}//TEMP_NAME
	//else if(token=="END") return NULL;
	else {
		error(line,"there is no IF WHILE READ RETURN ID WRITE to match");
		read_token();
		return NULL;
	}
}
Node *StmMore(){//只争对两个循环
	//output<<"StmMore"<<endl;
	if(token==";"){//出现了分号说明后面一定还有句子
		read_token();
		return StmList();
	}
	else if(token=="END"||token=="ENDWH"||token=="FI"||token=="ELSE"){//
		//output<<"!!!"<<endl;
		//read_token();
		return NULL;
	}
	else {
//
		error(line,"there is no correct to match1");output<<" "<<token<<endl;return NULL;
		read_token();
	}
}
Node *StmList(){//进入时是语句第一个词
	//output<<"StmList"<<endl;
	if(token=="END") return NULL;
	Node *t=Stm();//退出时要求语句第一个词还没有读入 ，即还是上一条语句的最后一词 ；或ENDWH FI ELSE END的下一个
	//read_token();
	//output<<"------------------"<<token<<endl;
	Node *p=StmMore();
	t->sibling=p;
	return t;
}
Node *program_body(){
	//output<<"program_body"<<endl;
	Node *t=init_node();t->nodekind=StmLK;
	if(token=="BEGIN"){
		read_token();
		//output<<"!!!!!"<<endl;
		t->child[0]=StmList();
		//output<<"!!!!!!!"<<endl;
	}
	else {
		error(line,"there is no BEGIN to match");
		//read_token();
	}
	if(token!="END") error(line,"there is no END to match");
	read_token();
	return t;
}
////////////////////////////////program_body部分

//////////////////////////////过程声明部分分析程序begin
Node *ProcBody(){
	//output<<"ProcBody"<<endl;
	Node *t= program_body();
	if(t==NULL) error(line,"there is no program_body");
	return t;
}
Node *ProcDecPart(){
	//output<<"ProcDecPart"<<endl;
	return declare_part();
}
Node *ParamMore(){
	//output<<"ParamMore"<<endl;
	//if(has_unread==false)read_token();has_unread=false;
	if(token==")") return NULL;
	else if(token==";") {//最后一个参数声明没有;直接是）
		read_token();
		Node *p=ParamDecList();
		if(p==NULL) error(line,"there is no ParamDecList or there is ; not nessesary");
		return p;
	}
	else {
		error(line,"there is no ) ; to match");
		read_token();
		return NULL;
	}
}
void FidMore(Node *t){// 处理 integer a,b中这种有,的情况
	//output<<"FidMore"<<endl;
	//read_token();
	if(token==","){read_token();FormList(t);}
	else if(token==")"||token==";"){return;}
	else {
		error(line,"there is no , ) ; to match");
		read_token();
	}
}
void FormList(Node *t){//处理一系列a,b,c,dz
	//output<<"FormList"<<endl;
	//read_token();
	if(type=="ID"){
		t->name[t->idnum++]=token;read_token();
	}
	else error(line,"there is no ID to match");
	FidMore(t);
}
Node *Param(){//一个param是两个分号内的参数
	//output<<"Param"<<endl;
	Node *t=init_node();t->nodekind=DecK;
	if(token=="VAR"){
		t->attr.ProcAttr.paramt=varparamType;
		read_token();TypeName(t);FormList(t);
	}
	else if(token=="CHAR"||token=="INTEGER"||token=="ARRAY"||token=="RECORD"||type=="ID"){
		t->attr.ProcAttr.paramt=valparamType;
		TypeName(t);FormList(t);
	}
	else {
		error(line,"there is no BaseType or TypeName or VAR to match");
		read_token();
	}
	return t;
}
Node *ParamDecList(){
	//output<<"ParamDecList"<<endl;
	Node *t=Param();
	Node *p=ParamMore();
	t->sibling=p;
	return t;
}
void ParamList(Node *t){//函数定义参数部分
	//output<<"ParamList"<<endl;
	//read_token();
	if(token==")"){ read_token();return;}
	else if(token=="CHAR"||token=="INTEGER"||token=="ARRAY"||token=="RECORD"||type=="ID"||token=="VAR"){//VAR是引用
		t->child[0]=ParamDecList();
	}
	else {
		error(line,"there is no BaseType ) to match");
		read_token();
	}
}
Node *ProcDeclaration(){//t->sibling是新加的
	//output<<"ProcDeclaration"<<endl;
	Node *t=init_node();t->nodekind=ProcDecK;
	if(token!="PROCEDURE") error(line,"there is no PROCEDURE to match");
	read_token();
	if(type=="ID"){
		t->name[t->idnum++]=token;
		read_token();
	}
	else error(line,"there is no ID to match");

	if(token!="("){error(line,"there is no ( to match");}
	read_token();ParamList(t);
	if(token!=")"){error(line,"there is no ) to match");}
	read_token();if(token!=";"){error(line,"there is no ; to match");}
	read_token();
	t->child[1]=ProcDecPart();
		//output<<"!!!!!!"<<endl;
	t->child[2]=ProcBody();
	t->sibling=ProcDec();
	return t;
	//
}
Node *ProcDec(){
	//output<<"ProcDec"<<endl;
	if(token=="BEGIN") return NULL;
	else if(token=="PROCEDURE"){
		return ProcDeclaration();
	}
	else {
		error(line,"there is no BEGIN PROCEDURE to match");
		read_token();
		return NULL;
	}
}
///////////////////////////////过程声明部分分析程序end

//////////////////////////////变量声明部分分析程序begin
Node* VarDecMore(){
	//output<<"VarDecMore"<<endl;
	//read_token();
	if(token=="PROCEDURE"||token=="BEGIN") return NULL;
	else if(token=="CHAR"||token=="INTEGER"||token=="ARRAY"||token=="RECORD"||type=="ID"){
		return VarDecList();
	}
	else {
		error(line,"there is no BaesType PROGRAM BEGIN to macth");
		read_token();
		return NULL;
	}
}
void VarIdMore(Node *t){
	//output<<"VarIdMore"<<endl;
	//read_token();
	if(token==";") return ;
	else if(token==","){read_token();VarIdList(t);}
	else {
		error(line,"there is no ; , to macth");
		read_token();
	}
}
void VarIdList(Node *t){
	//output<<"VarIdList"<<endl;
	//read_token();
	if(type=="ID") {t->name[t->idnum++]=token;read_token();}
	else {
		error(line,"there is no ID to match");
		read_token();
	}
	VarIdMore(t);
}
Node *VarDecList(){
	//output<<"VarDecList"<<endl;
	Node *t=init_node();t->nodekind=DecK;
	//if(has_unread==false) read_token();has_unread=false;
	if(token=="CHAR"||token=="INTEGER"||token=="ARRAY"||token=="RECORD"||type=="ID"){
		TypeName(t);
		VarIdList(t);
		if(token!=";") error(line,"there is no ; to match");
		read_token();
		t->sibling=VarDecMore();
		return t;
	}
	else {
		error(line,"there is no TypeName to match");
		read_token();
		return NULL;
	}
}
Node *VarDeclartion(){
	//output<<"VarDeclartion"<<endl;
	if(token!="VAR")error(line,"there is no VAR to match");
	read_token();
	Node *t=VarDecList();
	if(t==NULL) error(line,"there is no VarDecList ");
	return t;
}
Node *VarDec(){
	//output<<"VarDec"<<endl;
	if(token=="PROCEDURE"||token=="BEGIN") return NULL;
	else if(token=="VAR"){ return VarDeclartion();}
	else {
		error(line,"there is no PROCEDURE or BEGIN or VAR to match");
		read_token();
		return NULL;
	}
}
///////////////////////////////变量声明部分分析程序end


//////////////////////////////类型声明处理分析程序 begin
Node *TypeDecMore(){
	//output<<"TypeDecMore"<<endl;
	//read_token();
	if(token=="VAR"||token=="PROGRAM"||token=="BEGIN"){	return NULL;}
	else if(type=="ID") {return TypeDecList();}
	else {
		error(line,"there is no VAR or PROGRAM or BEGIN or ID to match");
		read_token();
		return NULL;
	}
}
void IdMore(Node *t){
	//output<<"IdMore"<<endl;
	//read_token();
	if(token==",") {read_token();IdList(t);}
	else if(token==";"){return ;}
	else {
		error(line,"there is no , ; to match");
		read_token();
	}
}
void IdList(Node *t){/////read_token()部分不一样
	//output<<"IdList"<<endl;
	//read_token();
	if(type=="ID"){t->name[t->idnum++]=token;}//
	else error(line,"there is no ID to match");
	read_token();
	IdMore(t);
}
Node *FieldDecMore(){
	//output<<"FieldDecMore"<<endl;
	//read_token();
	if(token=="END") {return NULL;}
	else if(token=="INTEGER"||token=="CHAR"||token=="ARRAY"){
		return FieldDecList();
	}
	else {
		error(line,"there is no END or INTGER or CHAR or ARRAY to match");
		read_token();
		return NULL;
	}
}
Node *FieldDecList(){//域成员记录函数
	//output<<"FieldDecList"<<endl;
	Node *t=init_node();t->nodekind=DecK;
	//read_token();
	if(token=="INTEGER"||token=="CHAR"){
		BaseType(t);IdList(t);
		if(token!=";") error(line,"there is no ; to match");
		read_token();
		t->sibling=FieldDecMore();
		return t;
	}
	else if(token=="ARRAY"){
		ArrayType(t);IdList(t);
		if(token!=";") error(line,"there is no ; to match");
		read_token();
		t->sibling=FieldDecMore();
		return t;
	}
	else {
		error(line,"there is no INTEGER or CHAR or ARRAY to match");
		read_token();
		return NULL;
	}
}
void RecType(Node *t){
	//output<<"RecType"<<endl;
	if(token!="RECORD") error(line,"there is no RECORD to match");
	read_token();
	Node *p=FieldDecList();
	if(p==NULL) error(line,"there is no FieldDecList");
	else t->child[0]=p;
	if(token!="END") error(line,"there is no END to match");
	read_token();
}
void ArrayType(Node *t){
	//output<<"ArrayType"<<endl;
	if(token!="ARRAY")error(line,"there is no ARRAY to match");
	read_token();if(token!="[") {error(line,"there is no [ to match");}
	read_token();
	if(type=="INTC") t->attr.ArrayAttr.low=atoi(token.c_str());
	else {error(line,"there is no integer to match");}
	read_token();if(token!="..") {error(line,"there is no .. to match");}
	read_token();
	if(type=="INTC") t->attr.ArrayAttr.up=atoi(token.c_str());
	else {error(line,"there is no integer to match");}
	read_token();if(token!="]") {error(line,"there is no ] to match");}
	read_token();if(token!="OF") {error(line,"there is no OF to match");}
	read_token();BaseType(t);
	t->attr.ArrayAttr.childtype=t->kind.dec;
	t->kind.dec=ArrayK;//kind.dec本来是array但是在数组基本类型的时候会被覆盖成基本类型的kind.dec，所以现在要改回来
}
void StructureType(Node *t){
	//output<<"StructureType"<<endl;
	if(token=="ARRAY") {t->kind.dec=ArrayK;ArrayType(t);}
	else if(token=="RECORD") {t->kind.dec=RecordK;RecType(t);}
	else read_token();
}
void BaseType(Node *t){
	//output<<"BaseType"<<endl;
	if(token=="INTEGER") t->kind.dec=IntegerK;
	else if(token=="CHAR") t->kind.dec=CharK;
	read_token();
}
void TypeName(Node *t){
	//output<<"TypeName"<<endl;
	//if(has_unread==false)read_token();has_unread=false;
	if(token=="INTEGER"||token=="CHAR"){BaseType(t);}
	else if(token=="ARRAY"||token=="RECORD"){StructureType(t);}
	else if(type=="ID") {t->kind.dec=IdK;t->attr.type_name=token;read_token();}
	else {
		error(line,"there is no match for TypeName");
		read_token();
	}
}
void TypeId(Node *t){
	//output<<"TypeId"<<endl;
	//if(has_unread==false) read_token();has_unread=false;
	if(type=="ID") t->name[t->idnum++]=token;
	else error(line,"there is no match for ID");
	read_token();
}
Node *TypeDecList(){
	//output<<"TypeDecList"<<endl;
	Node *t=init_node();t->nodekind=DecK;
	TypeId(t);
	if(token!="=") {error(line,"there is no match for =");}
	read_token();TypeName(t);
	if(token!=";") {error(line,"there is no match for ;");}
	read_token();Node *p=TypeDecMore();
	t->sibling=p;
	return t;
}
Node *TypeDeclaration(){
	//output<<"TypeDeclaration"<<endl;
	if(token!="TYPE") error(line,"there is no TYPE to match");
	read_token();
	Node *t=TypeDecList();
	if(t==NULL) error(line,"there is no TypeDecList to match");
	return t;
}
Node *TypeDec(){
	//output<<"TypeDec"<<endl;
	Node *t=init_node();
	if(token=="TYPE") return TypeDeclaration();
	else if(token=="VAR"||token=="PROCEDURE"||token=="BEGIN"){	return NULL;}
	else {
		error(line,"there is some key_word missing in declare_part");
		read_token();
		return NULL;
	}
}
///////////////////////////////类型声明处理分析程序end

Node *declare_part(){
	//read_token();
	Node *type_t=init_node();type_t->nodekind=TypeK;type_t->child[0]=TypeDec();
	Node *var_t=init_node();var_t->nodekind=VarK;var_t->child[0]=VarDec();
	Node *proc_deck_t=init_node();proc_deck_t->nodekind=ProcDecK;proc_deck_t->child[0]=ProcDec();



	type_t->sibling=var_t;var_t->sibling=proc_deck_t;
	return type_t;
}
Node * program_head(){
	Node *t=init_node();t->nodekind=PheadK;
	if(token!="PROGRAM"){error(line,"no correct program_head");}
	read_token();
	if(type=="ID") {t->name[0]=token;}
	else error(line,"no correct program_head");
	read_token();
	return t;
}

Node* program(){
	Node *t=program_head();
	Node *q=declare_part();
	Node *s=program_body();
	Node *root=init_node();root->nodekind=ProK;
	root->child[0]=t; root->child[1]=q; root->child[2]=s;
	if(token!=".") error(line,"there id no . in the end");
	read_token();
	return root;
}
Node* parse(){
	read_token();
	Node *t=program();
	if(token!="EOF") {error(line,"bad end");}
	return t;
}
int main(){
	input.open("../data/token.txt");
	if(!input) {output<<"Error:cannot find or open the specified file!";return 0;}
	output.open("../data/syntax_tree.txt");
	if(!output) {output<<"Error:cannot find or open the specified file!";return 0;}
	Node *head=parse();
	print_tree(head,0);
}
}

