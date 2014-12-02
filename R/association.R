# load necessary libraries
library(ggplot2) 
library(arules)
library(arulesViz)
##########################################
## Unique page hits
##########################################
# load page hit data
system.time(transactions <- read.transactions("assets/unique_pagehits.csv", format="basket", sep=","))
summary(transactions)
itemFrequency(transactions)

# plot frequency of each category
itemFrequencyPlot(transactions, support=0.001)

# find rules that have minimum support and confidence = 1% and 70%
system.time(rules <- apriori(transactions, parameter = list(supp=0.01, conf=0.30, minlen=2)))
summary(rules)

# find 2-itemset rules that have minimum support and confidence being 1\% and 35\%
system.time(rules <- apriori(transactions, parameter = list(supp=0.02, conf=0.35, minlen=2, maxlen=2)))

system.time(rules <- apriori(transactions, parameter = list(supp=0.01, conf=0.01), appearance = list(lhs = c("frontpage","business","local","news","on-air","sports","tech"), default="lhs") ))

# find rules that have rhs=Front page
system.time(rules <- apriori(transactions, parameter = list(supp=0.01, conf=0.01), appearance = list(lhs = c("frontpage"), default="lhs") )

inspect(sort(rules, by="support"))
plot(rules, measure="support", shading="lift")
plot(rules, measure=c("support","lift"), shading="confidence")
plot(rules, shading="order", control=list(main="Two-key plot"))

# interactive plot
sel <- plot(rules, measure=c("support","lift"), shading="confidence", interactive=TRUE)

plot(rules, method="matrix", measure="lift")
plot(rules, method="matrix", measure="lift", control=list(reorder=TRUE))
plot(rules, method="matrix", measure=c("lift","confidence"))
plot(rules, method="matrix", measure=c("lift","confidence"), control=list(reorder=TRUE))
plot(rules, method="grouped")
plot(rules, method="grouped", control=list(k=50))

sorted <- sort(rules, by="support")
plot(sorted, method="graph", control=list(type="items"))

sortedByLift <- sort(rules, by="lift")
plot(sorted, method="graph", control=list(type="items"))

plot(sorted, method="paracoord")
plot(sorted, method="paracoord", control=list(reorder=TRUE))


plot(rules, method="matrix3D", measure="lift")
plot(rules, method="matrix3D", measure="lift", control=list(reorder=TRUE))



#interestMeasure(rules, c("support", "chiSquare", "confidence", "cosine", "coverage", "lift"), transactions)


            
         
