install.packages("exact2x2")
install.packages("effectsize")
install.packages("xtable")

library(exact2x2)
library(effsize)
library(xtable)

datasets=c("method_calls", "class_signatures", "most_similar_method", "issue_title", "issue_body", "frequent_invocations",
            "most_similar_statements", "method_calls_class_signatures", "most_similar_method_method_calls", "most_similar_method_class_signatures",
            "most_similar_method_method_calls_class_signatures", "issue_title_issue_body", "frequent_invocations_most_similar_statements",
            "best_code_best_process", "best_code_best_developer",
            "best_developer_best_process", "best_code_best_developer_best_process", "confidence_model")


res=list(Dataset=c(),McNemar.p=c(),McNemar.OR=c())

for(d in datasets)
{
  nameFile=paste("mcnemar/Mcnemar_",d,".csv",sep="")
  t<-read.csv(nameFile)
  
  m=mcnemar.exact(t$Baseline,t$Context)
  res$Dataset=c(res$Dataset,as.character(d))
  
  res$McNemar.p=c(res$McNemar.p,m$p.value)
  res$McNemar.OR=c(res$McNemar.OR,m$estimate)
  

}

res=data.frame(res)
res2=res
#p-value adjustment
res2$McNemar.p=p.adjust(res2$McNemar.p,method="BH")
print(xtable(res2),include.rownames=FALSE)

print(res2)