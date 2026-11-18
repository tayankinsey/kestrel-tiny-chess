_F='pnbrqk'
_E=False
_D=None
_C='P'
_B='K'
_A=True
import os,time
from itertools import count
from collections import namedtuple
__version__='2026-packed'
version='sunfish '+__version__
piece={_C:100,'N':280,'B':320,'R':479,'Q':929,_B:60000}
pst={_C:(0,0,0,0,0,0,0,0,78,83,86,73,102,82,85,90,7,29,21,44,40,31,44,7,-17,16,-2,15,14,0,15,-13,-26,3,10,9,6,1,0,-23,-22,9,5,-11,-10,-2,3,-19,-31,8,-7,-37,-36,-14,3,-31,0,0,0,0,0,0,0,0),'N':(-66,-53,-75,-75,-10,-55,-58,-70,-3,-6,100,-36,4,62,-4,-14,10,67,1,74,73,27,62,-2,24,24,45,37,33,41,25,17,-1,5,31,21,22,35,2,0,-18,10,13,22,18,15,11,-14,-23,-15,2,0,2,0,-23,-20,-74,-23,-26,-24,-19,-35,-22,-69),'B':(-59,-78,-82,-76,-23,-107,-37,-50,-11,20,35,-42,-39,31,2,-22,-9,39,-32,41,52,-10,28,-14,25,17,20,34,26,25,15,10,13,10,17,23,17,16,0,7,14,25,24,15,8,25,20,15,19,20,11,6,7,6,20,16,-7,2,-15,-12,-14,-15,-10,-10),'R':(35,29,33,4,37,33,56,50,55,29,56,67,55,62,34,60,19,35,28,33,45,27,25,15,0,5,16,13,18,-4,-9,-6,-28,-35,-16,-21,-13,-29,-46,-30,-42,-28,-42,-25,-25,-35,-26,-46,-53,-38,-31,-26,-29,-43,-44,-53,-30,-24,-18,5,-2,-18,-31,-32),'Q':(6,1,-8,-104,69,24,88,26,14,32,60,-10,20,76,57,24,-2,43,32,60,72,63,43,2,1,-16,22,17,25,20,-13,-6,-14,-15,-2,-5,-1,-10,-20,-22,-30,-6,-13,-11,-16,-11,-16,-27,-36,-18,0,-19,-15,-15,-21,-38,-39,-30,-31,-13,-31,-36,-34,-42),_B:(4,54,47,-99,-99,60,83,-62,-32,10,55,56,56,55,10,3,-62,12,-57,44,-67,28,37,-31,-55,50,11,-4,-19,13,0,-49,-55,-43,-52,-28,-51,-47,-8,-50,-47,-42,-43,-79,-64,-32,-29,-32,-4,3,-14,-50,-57,-18,13,4,17,30,-3,-14,6,-1,40,18)}
for(k,table)in pst.items():padrow=lambda row:(0,)+tuple(A+piece[k]for A in row)+(0,);pst[k]=sum((padrow(table[A*8:A*8+8])for A in range(8)),());pst[k]=(0,)*20+pst[k]+(0,)*20
K_MID,K_END=pst[_B],tuple(piece[_B]+70-10*(abs(2*(A//10)-11)+abs(2*(A%10)-9))for A in range(120))
MATE_LOWER=47923
MATE_UPPER=69290
A1,H1,A8,H8=91,98,21,28
initial='         \n         \n rnbqkbnr\n pppppppp\n ........\n ........\n ........\n ........\n PPPPPPPP\n RNBQKBNR\n         \n         \n'
N,E,S,W=-10,1,10,-1
directions={_C:(N,N+N,N+W,N+E),'N':(N+N+E,E+N+E,E+S+E,S+S+E,S+S+W,W+S+W,W+N+W,N+N+W),'B':(N+E,S+E,S+W,N+W),'R':(N,E,S,W),'Q':(N,E,S,W,N+E,S+E,S+W,N+W),_B:(N,E,S,W,N+E,S+E,S+W,N+W)}
QS=40
QS_A=140
EVAL_ROUGHNESS=15
PROBE_CAP=40
LMR=60
TABLE_SIZE=10**6
opt_ranges=dict(QS=(0,300),QS_A=(0,300),EVAL_ROUGHNESS=(0,50),TABLE_SIZE=(10**4,10**8))
Move=namedtuple('Move','i j prom')
class Position(namedtuple('Position','board score wc bc ep kp')):
	def __hash__(A):return hash((A.board,A.wc,A.bc,A.ep,A.kp))
	def __eq__(A,o):return A.board==o.board and A.ep==o.ep and A.kp==o.kp and A.wc==o.wc and A.bc==o.bc
	def __ne__(A,o):return not A.__eq__(o)
	def gen_moves(A):
		for(C,F)in enumerate(A.board):
			if F not in'PNBRQK':continue
			for D in directions[F]:
				for B in count(C+D,D):
					G=A.board[B]
					if G in' \nPNBRQK':break
					if F==_C:
						if D in(N,N+N)and G!='.':break
						if D==N+N and(C<A1+N or A.board[C+N]!='.'):break
						if D in(N+W,N+E)and G=='.'and B not in(A.ep,A.kp,A.kp-1,A.kp+1):break
						if A8<=B<=H8:
							for H in'NBRQ':yield Move(C,B,H)
							break
					yield Move(C,B,'')
					if F in'PNK'or G in _F:break
					if C==A1 and A.board[B+E]==_B and A.wc[0]:yield Move(B+E,B+W,'')
					if C==H1 and A.board[B+W]==_B and A.wc[1]:yield Move(B+W,B+E,'')
	def rotate(A,nullmove=_E):B=nullmove;return Position(A.board[::-1].swapcase(),-A.score,A.bc,A.wc,119-A.ep if A.ep and not B else 0,119-A.kp if A.kp and not B else 0)
	def move(D,move):
		C,B,K=move;J,O=D.board[C],D.board[B];E=lambda board,i,p:board[:i]+p+board[i+1:];A=D.board;F,G,I,H=D.wc,D.bc,0,0;L=D.score+D.value(move);A=E(A,B,A[C]);A=E(A,C,'.');F=F[0]and C!=A1,F[1]and C!=H1;G=G[0]and B!=H8,G[1]and B!=A8
		if J==_B:
			F=_E,_E
			if abs(B-C)==2:H=(C+B)//2;M=A1 if B<C else H1;A=E(A,M,'.');A=E(A,H,'R')
		if J==_C:
			if A8<=B<=H8:A=E(A,B,K)
			if B-C==2*N:I=C+N
			if B==D.ep:A=E(A,B+S,'.')
		return Position(A[::-1].swapcase(),-L,G,F,119-I if I else 0,119-H if H else 0)
	def value(D,move):
		C,A,G=move;E,F=D.board[C],D.board[A];B=pst[E][A]-pst[E][C]
		if F in _F:B+=pst[F.upper()][119-A]
		if abs(A-D.kp)<2:B+=pst[_B][119-A]
		if E==_B and abs(C-A)==2:B+=pst['R'][(C+A)//2];B-=pst['R'][A1 if A<C else H1]
		if E==_C:
			if A8<=A<=H8:B+=pst[G][A]-pst[_C][A]
			if A==D.ep:B+=pst[_C][119-(A+S)]
		return B
	def king_capture(A):return next((B for B in A.gen_moves()if A.board[B.j]=='k'or abs(B.j-A.kp)<2),_D)
class Stop(Exception):0
Entry=namedtuple('Entry','lower upper')
class Searcher:
	def __init__(A):A.tp_score,A.tp_move,A.history={},{},set();A.nodes,A.deadline=0,1<<63;A.node_cap=1<<62
	def bound(B,pos,gamma,depth,root=_E):
		I=root;D=gamma;C=depth;A=pos;B.nodes+=1
		if B.nodes%2048==0 and B.nodes>B.node_cap:raise Stop
		if B.nodes%2048==0 and time.time()>B.deadline:raise Stop
		C=max(C,0)
		if A.score<=-MATE_LOWER:return-MATE_UPPER
		if not I:
			F=B.tp_score.get((A,C),Entry(-MATE_UPPER,MATE_UPPER))
			if F.lower>=D:return F.lower
			if F.upper<D:return F.upper
			if C>0 and A in B.history:return 0
		def K():
			F=B.tp_move.get(A)
			if not I and C>2 and abs(A.score)<500 and any(B in A.board for B in'RBNQ'):
				E=-B.bound(A.rotate(nullmove=_A),1-D,C-3);J=E>=D and(B.tp_move.get(A)or A.king_capture())
				if J and A.value(J)>=MATE_LOWER:yield(J,MATE_UPPER)
				elif E<D or B.bound(A.rotate(nullmove=_A),1-MATE_LOWER,C-3)>=1-MATE_LOWER:yield(_D,E)
			if C==0:yield(_D,A.score)
			if not F and C>2:B.bound(A,D,C-3,root=_A);F=B.tp_move.get(A)
			K=QS-C*QS_A
			if F and A.value(F)>=K:yield(F,-B.bound(A.move(F),1-D,C-1))
			for(M,(G,H))in enumerate(sorted(((N,B)for B in A.gen_moves()if(N:=A.value(B))>=K),reverse=_A)):
				if C<=1 and A.score+G<D:yield(H,MATE_UPPER)if G>=MATE_LOWER else(_D,A.score+G);break
				L=LMR and C>2 and M>2 and G<LMR;E=-B.bound(A.move(H),1-D,C-2 if L else C-1)
				if L and E>=D:E=-B.bound(A.move(H),1-D,C-1)
				yield(H,E)
		E,H=-MATE_UPPER,_E
		for(G,J)in K():
			E=max(E,J);H|=G is not _D and J>-MATE_UPPER
			if E>=D:
				if G is not _D and C:
					B.tp_move[A]=G
					if len(B.tp_move)>TABLE_SIZE:del B.tp_move[next(A for A in B.tp_move if A!=B.root)]
				break
		if C and not H and all(A.move(B).king_capture()for B in A.gen_moves()):E=-MATE_LOWER if A.rotate(nullmove=_A).king_capture()else 0
		if not I:B.tp_score[A,C]=Entry(E,F.upper)if E>=D else Entry(F.lower,E)
		if len(B.tp_score)>TABLE_SIZE:del B.tp_score[next(iter(B.tp_score))]
		return E
	def search(C,history):
		K='upper';J='lower';I=history;C.nodes,C.history=0,set(I);C.tp_score.clear();D=C.root=I[-1];L=sum(A.isupper()for A in D.board)==1 or sum(A.islower()for A in D.board)==1;pst[_B]=K_END if L else K_MID;E=0
		for F in range(1,1000):
			A,B,H=1-MATE_UPPER,MATE_UPPER,0
			while A<B-EVAL_ROUGHNESS:
				G=C.bound(D,E,F,root=_A)
				if G>=E:A=max(A,G)
				else:B=min(B,G)
				H+=1;yield(F,E,G,C.tp_move.get(D))
				if A>B or H>PROBE_CAP:
					if H>PROBE_CAP:print('info string MTD-GUARD probe cap hit: depth',F,J,A,K,B,flush=_A)
					if A>B:print('info string MTD-GUARD bracket crossed: depth',F,J,A,K,B,flush=_A)
					break
				E=(A+B+1)//2
def parse(c):return A1+ord(c[0])-ord('a')-10*(int(c[1])-1)
def render(i):return chr((i-A1)%10+ord('a'))+str(1-(i-A1)//10)
def from_board(board,wc=(_A,_A),bc=(_A,_A),ep=0,kp=0,pf=0):A=board;B=sum(pst[A][B]if A.isupper()else-pst[A.upper()][119-B]for(B,A)in enumerate(A)if A.isalpha());return Position(A,B,wc,bc,ep,kp)
import json as _json,os as _os,urllib.request as _rq
def post(path,body):A=_rq.Request(_os.environ['MAKEFUN_ENV_URL']+path,_json.dumps(body).encode(),{'content-type':'application/json'});return _json.load(_rq.urlopen(A))
def uci_to_move(u,hist):
	A,B=parse(u[:2]),parse(u[2:4])
	if len(hist)%2==0:A,B=119-A,119-B
	return Move(A,B,u[4].upper()if len(u)>4 else'')
def move_to_uci(mv,hist):
	A,B=mv.i,mv.j
	if len(hist)%2==0:A,B=119-A,119-B
	return render(A)+render(B)+(mv.prom.lower()if mv.prom else'')
NODE_BUDGET=100000
def play_games():
	I='game';H='your_move';G='status'
	while _A:
		A=post('/game',{})
		if A.get(G)!=H:break
		while A.get(G)==H:
			B=[from_board(initial)]
			for K in A['moves']:B.append(B[-1].move(uci_to_move(K,B)))
			E=Searcher();E.node_cap=NODE_BUDGET;C=_D
			try:
				for(M,N,O,L)in E.search(B):C=L
			except Stop:0
			F=A['legal_moves'];D=move_to_uci(C,B)if C else''
			if D not in F:D=sorted(F)[0]
			A=post('/move',{I:A[I],'move':D})
play_games()
