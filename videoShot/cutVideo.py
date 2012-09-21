import os
import time         

class CutVideo(object):
    
    
    def cut_video(self,file_name, file_video_save, corte, x):
        for i in range(len(corte)-1):
            inicio = corte[i]
            duracao = corte[i + 1] - inicio - 0.2
            os.system("ffmpeg -i " + str(file_name) + " -ss " + str(inicio) + " -t " + str(duracao) + " -acodec copy -vcodec copy -ar 22050 " + str(file_video_save) + "cpu_"+str(x)+ "_part_" + str(i + 1) + ".ogg > /dev/null 2>&1")      
                       
    def position_cut_list(self,cut_list,ncpus):
        #Algoritimo para separar os segmentos em intervalos minimos de 10s
        new_cut_list=[]
        actual_time = cut_list[0]
        cont = 0
        new_cut_list.append(cut_list[0])
        while cont < len(cut_list):
            if cut_list[cont] - actual_time >= 10:
                actual_time = cut_list[cont]
                new_cut_list.append(cut_list[cont])
            cont+=1
             
        #if utilizado para tratar erro quando a lista nova nao possui o ultimo intervalo de tempo que a lista velha possuia, 
        #isso ocorre porque o ultimo intervalo de tempo pode ser menor que 10 s       
        if new_cut_list[len(new_cut_list)-1] != cut_list[len(cut_list)-1]:
            new_cut_list.append(cut_list[len(cut_list)-1]) 

        #if utilizado para tratar erro que ocorre quando a nova lista possui um segmento de menos de 10 s no final da lista
        if new_cut_list[len(new_cut_list)-1] - new_cut_list[len(new_cut_list)-2] <10:
            del new_cut_list[len(new_cut_list)-2]     
        corte = []
        parametro = len(new_cut_list)/ncpus
        elemento=0
        #Algoritimo utilizado para dividir os tempos para corte em listas de acordo com a quantidade de cpus
        for x in range(ncpus):
            corte.append([])
            for y in range(parametro+1):
                if elemento < len(new_cut_list):
                    corte[x].append(new_cut_list[elemento])
                    elemento+=1
            elemento-=1    
        #If utilizado para tratar erro de divisao
        if len(new_cut_list) % ncpus !=0 and len(new_cut_list) % ncpus !=1:
            corte[ncpus-1].extend(new_cut_list[-(len(new_cut_list) - (ncpus * parametro+1)):])
        return corte 
    
