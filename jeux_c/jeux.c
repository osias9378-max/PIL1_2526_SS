#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <time.h>

struct number{
   int a[3];
};
struct couple{
   int a,b;
};
struct chiffre{
   int a[10];
};
typedef struct chiffre chiffre;

typedef struct couple couple;

typedef struct number number;

typedef enum{faux,vrai} boolean;

number transform(int nb){
   number tab;
   for(int i = 2;i>=0;i--){
      tab.a[i] = nb % 10;
      nb = nb/10;
   }
   return tab;
}

boolean pre_verify(int use_try){
   if(100>use_try || use_try>999){
      printf("Entrer invalide veuillez entrez un nombre a Trois chiffre");
      return faux;
   }
   number use = transform(use_try);
   if(use.a[2] == use.a[1]){
      printf("ERREUR!!!!!!!!:Le chiffre des unites et celui des dizaines sont egaux.LES TROIS CHIFFRES DOIVENT ETRE DISTINCTS\n");
      return faux ;
   }
   if(use.a[2] == use.a[0]){
      printf("ERREUR!!!!!!!!!: Le chiffre des unites et celui des centaines sont egaux.LES TROIS CHIFFRES DOIVENT ETRE DISTINCTS\n");
      return faux ;
   }
   if(use.a[0] == use.a[1]){
      printf("ERREUR!!!!!!!!!: Le chiffre des dizaines et celui des centaines sont egaux.LES TROIS CHIFFRES DOIVENT ETRE DISTINCTS\n");
      return faux;
   }
   printf("parfait\n");
   return vrai;
}

number penser(chiffre bibli){
   number tab ;
   tab.a[0] =(rand() % 9) + 1;
   do{
      tab.a[1] = rand() % 10;
   }while(tab.a[1] == tab.a[0]);
   do{
      tab.a[2] = rand() % 10; 
   } while (tab.a[1] == tab.a[2] || tab.a[2] == tab.a[0]);
   for(int i=0;i<3;i++){
      tab.a[i] = bibli.a[tab.a[i]];
   }
   int numb = tab.a[0] *100 +tab.a[1] *10 + tab.a[2];
   if (!pre_verify(numb)){
      penser(bibli);
      return tab;
   }
   return tab;  
}

void afficher(number tab){
   for(int i = 0;i<3;i++){
      printf("%d",tab.a[i]);
   }
   printf("\n");
}


chiffre parabibli(chiffre bibli,int  nombre){
   int m;
   do
      m = rand() % 10;
   while(m == bibli.a[nombre]);   
   bibli.a[nombre] = m;
   return bibli;
}


couple verify(number user,number tab){
   couple check;
   check.a = 0;
   check.b = 0;
   for(int i = 0;i<3;i++){
      for(int j= 0;j<3;j++){
         if(user.a[i] == tab.a[j])
            check.a = check.a + 1;
         if(user.a[j]==tab.a[j])
            check.b = check.b + 1;
      }
   }
   return check;
}
number transposer(number first){
   int help = first.a[1];
   first.a[1] = first.a[2];
   first.a[1] = help;
   return first; 
}

number transposer_bis(number first){
   int help = first.a[1];
   first.a[1] = first.a[0];
   first.a[0] = help;
   return first; 
}



number search(number furst,number first , couple out_us,couple out_pre,chiffre bibli){
   int m = rand() % 10;
   if(out_us.a == 3){
      if(out_us.b == 0 ){
         int help = first.a[0];
         if(first.a[2]!=0){
            first.a[0] = first.a[2];
            first.a[2] = first.a[1];
            first.a[1] = help; 
            return first ;
         }
         first.a[0] = first.a[1];
         first.a[1] = first.a[2];
         first.a[2] = help; 
         return first ;
      }
      if(out_us.b == 1){
         first = transposer(first);
         return first;
      }
   }
   if(out_us.a == 1){
      if(out_us.b == 0){
         if(out_pre.b == 0){
            int help = first.a[0];
            if(first.a[2]!=0){
               first.a[0] = first.a[2];
               first.a[2] = first.a[1];
               first.a[1] = help; 
               return first ;
           }
         }
      }
      if(out_us.b == 1 ){
         if(out_pre.b == out_pre.b){
            for (int i = 0;i<3;i++){
                  if(furst.a[i] == first.a[i]){
                     bibli = parabibli(bibli,furst.a[i]);
                     first.a[i] = bibli.a[m];
                     return first;
                  }
            }
         }
         for (int i = 0;i<3;i++){
               if(furst.a[i] != first.a[i]){
                  bibli = parabibli(bibli,furst.a[i]);
                  first.a[i] = bibli.a[m];
                  return first;
               }
         }
      }
   }
   if(out_us.a ==2){
      if(out_us.b ==0 || out_us.b == 1){
         if(out_pre.b == out_pre.b){
            int help = first.a[0];
            if(first.a[2]!=0){
               first.a[0] = first.a[2];
               first.a[2] = first.a[1];
               first.a[1] = help; 
               return first ;
            }
         }
      }
      if(out_us.b == 2 ){
         if(out_pre.b == 0 || out_pre.b == 1){
            for (int i = 0;i<3;i++){
               if(furst.a[i] == first.a[i]){
                  bibli = parabibli(bibli,furst.a[i]);
                  first.a[i] = bibli.a[m];
                  return first;
               }
            }
         }
         for (int i = 0;i<3;i++){
            if(furst.a[i] != first.a[i]){
               bibli = parabibli(bibli,furst.a[i]);
               first.a[i] = bibli.a[m];
               return first;
            }
         }
      }
   }
}


int main(){
   srand(time(NULL));
   number user,tab,now;
   chiffre bibli;
   for (int i = 0; i<10;i++){
      bibli.a[i] = i;
   }
   couple out,out_us;
   do
   {
      tab = penser(bibli);
      afficher(tab);
      printf("Combien de chiffres sont bon ????\n");
      scanf("%d",&out.a);
      if(out.a != 0){
         printf("Combien entre les %d sont bien place\n",out.a);
         scanf("%d",&out.b);
      }
      else{
         for (int i = 0;i<3;i++){
            bibli = parabibli(bibli,tab.a[i]);
         }
      }
   } while (out.a == 0);
   out_us = out;
   number pre = tab;
   user = pre;
   now = search(pre,user,out,out_us,bibli);
   
   while(out.b != 3){
      afficher(now);
      out_us = out;
      do
      {
         printf("Combien de chiffres sont bon ????\n");
         scanf("%d",&out.a);
         if(out.a != 0){
           printf("Combien entre les %d sont bien place",out.a);
           scanf("%d",&out.b);
         }
         else{
           for (int i = 0;i<3;i++){
                bibli = parabibli(bibli,tab.a[i]);
            }
         }
      } while (out.a == 0);
      pre = user;
      user = now;
     now = search(pre,user,out,out_us,bibli);
   }
   return 0;
}
