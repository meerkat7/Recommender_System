import math
import timeit
import numpy  as np
from numpy import linalg


def eigen(matrix):
	values,vectors=linalg.eig(matrix)
	answer={}
	l=len(values)
	for i in range(0,l):
		answer[values[i]]=vectors[:,i]
		
	values=sorted(values)
	fp={}
	for i in values:
		fp[round(i.real,2)]=answer[i].real
	return fp
  

def ponk_svd(mat,U,sigma,V):
	k=0
	trace=sigma.trace()
	sum_u=0
	sum_l=trace
	i=0
	while(sum_u<10*sum_l):
		sum_u=sum_u+sigma[i][i]
		sum_l=sum_l-sigma[i][i]
		k=k+1
		i=i+1
		if(i>len(sigma)-1):
			break
	print("\nPrecision on top ", k, " values.")
	while(k):
		x=len(sigma)-1
		sigma=np.delete(sigma,x,0)
		sigma=np.delete(sigma,x,1)
		U=np.delete(U,len(U[0])-1,1)
		V=np.delete(V,len(V.T[0])-1,0)
		k=k-1
	k_mat=(np.dot(U,np.dot(sigma,V)))
	for i in range(len(k_mat)):
		for j in range(len(k_mat[i])):
			k_mat[i][j]=round(k_mat[i][j],2)
	count=0.00
	match=0.00
	for i in range(0,len(mat)):
		for j in range(0,len(mat[i])):
			count=count+1
			a=int(round(mat[i][j]))
			b=int(round(k_mat[i][j]))
			if (a==b):
				match=match+1
	precision=(match*100)/count
	return precision

def srcr(mat,final):
	count=0
	sumds=0
	for i in range(0,len(mat)):
		for j in range(0,len(mat[i])):
			sumds=sumds+(mat[i][j]-final[i][j])**2
			count=count+1
	sumds=6*sumds
	den=(count**3)-count
	p=1-(sumds/den)
	return p

def rmse(matrix, final):
    error_rmse=0
    count=0
    for i in range(0,len(matrix)):
        for j in range(0,len(matrix[i])):
            error_rmse+=(matrix[i][j]-final[i][j])**2
            count+=1
    error_rmse=error_rmse/count
    error_rmse=math.sqrt(error_rmse)
    return error_rmse

def process(name):
	file=open(name,"r")
	raw=file.readlines()
	ratings=[]
	for line in raw:
		irate=[]
		line=line.split("\t")
		user=int(line[0])
		irate.append(user)
		movie=int(line[1])
		irate.append(movie)
		score_rate=float(line[2])
		irate.append(score_rate)
		ratings.append(irate)
	max_movie=0
	max_user=ratings[len(ratings)-1][0]
	for rate in ratings:
		if rate[1]>max_movie:
			max_movie=rate[1]
	rating_matrix=np.zeros((max_user, max_movie))
	for rate in ratings:
		rating_matrix[rate[0]-1][rate[1]-1]=rate[2]
	
	for i in range(len(rating_matrix)):
		sum=0
		count=0
		for j in range(len(rating_matrix[i])):
			sum=sum+rating_matrix[i][j]
			count=count+1.0
		avg=sum/count
		for k in range(len(rating_matrix[i])):
			rating_matrix[i][k]=rating_matrix[i][k]-avg

	rating_matrix=rating_matrix-rating_matrix.mean(axis=1,keepdims=True)
	return rating_matrix

def svd(matrix):
	matrix_T=matrix.transpose()
	A=np.dot(matrix,matrix_T)
	eigA=eigen(A)
	B=np.dot(matrix_T,matrix)
	eigB=eigen(B)
	answer=[]
	for key in eigA:
		if abs(key)!=0:
				round_key=round(key,2)
				answer.append(round_key)

	answer=sorted(answer,reverse=True)
	l=len(answer)
	leigA=len(eigA[answer[0]])
	leigB=len(eigB[answer[0]])
	U=np.zeros((leigA,l))
	V=np.zeros((leigB,l))
	
	for i in range(l):
		g=len(eigA[answer[i]])
		for j in range(g):
			U[j][i]=eigA[answer[i]][j]
		h=len(eigB[answer[i]])
		for j in range(h):
			V[j][i]=eigB[answer[i]][j]
	V=V.transpose()     
	sig=np.zeros((l,l))
	np.fill_diagonal(sig,answer,wrap=True)
	sig=np.sqrt(sig)
	ls=len(sig)
	for i in range(ls):
		row_matrix_V = V[i]
		row_matrix_V_matrix = np.matrix(row_matrix_V)
		row_matrix_V_transpose_matrix = row_matrix_V_matrix.T
		column_vector_v = np.dot(matrix, row_matrix_V_transpose_matrix)

		answer_u = []
		for row in U:
			column_count = 0
			for column in row:
				if column_count == i:
					answer_u.append(column)
					break
				column_count += 1

		u_vector = np.matrix(answer_u)
		u_column_vector = u_vector.T
		var = False
		V_length = len(column_vector_v) 

		for j in range(V_length):
			if u_column_vector[j] != 0.0:
				if column_vector_v[j]/u_column_vector[i] < 0.0:
					var = True
					break

		if var == True:    
			len_answer_u = len(answer_u)
			for k in range(len_answer_u):
				U[k][i]=-1.0*U[k][i]
	return U,sig,V


print("hello")
matrix=process("ratings.txt")
start=timeit.default_timer()
u,s,v=svd(matrix)
print(u)
print(s)
print(v)
final=(np.dot(u,np.dot(s,v)))
print("Time taken\n")
stop=timeit.default_timer()
print("%s seconds" %(stop-start))
rmse_err=rmse(matrix,final)
print("RMSE error is :")
print(rmse_err)
please=ponk_svd(matrix,u,s,v)
print(please)
answer=srcr(matrix,final)
print("spearman is ",answer)
