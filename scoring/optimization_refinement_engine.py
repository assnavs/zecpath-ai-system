class OptimizationRefinementEngine:
    """Validation metrics for labelled data; does not change production scoring thresholds."""
    @staticmethod
    def confusion_metrics(y_true,y_pred):
        if not isinstance(y_true,list) or not isinstance(y_pred,list) or not y_true or len(y_true)!=len(y_pred):
            raise ValueError("Labels must be non-empty lists of equal length.")
        if any(x not in (0,1) for x in y_true+y_pred): raise ValueError("Labels must be binary.")
        tp=sum(a==1 and b==1 for a,b in zip(y_true,y_pred)); tn=sum(a==0 and b==0 for a,b in zip(y_true,y_pred))
        fp=sum(a==0 and b==1 for a,b in zip(y_true,y_pred)); fn=sum(a==1 and b==0 for a,b in zip(y_true,y_pred))
        p=tp/(tp+fp) if tp+fp else 0; r=tp/(tp+fn) if tp+fn else 0
        return {"true_positive":tp,"true_negative":tn,"false_positive":fp,"false_negative":fn,
                "accuracy":round((tp+tn)/len(y_true),4),"precision":round(p,4),"recall":round(r,4),
                "f1_score":round(2*p*r/(p+r),4) if p+r else 0.0,"sample_count":len(y_true)}
    def evaluate_threshold(self,labelled_scores,threshold):
        if isinstance(threshold,bool) or not isinstance(threshold,(int,float)) or not 0<=threshold<=100:
            raise ValueError("threshold must be 0-100.")
        if not isinstance(labelled_scores,list) or not labelled_scores: raise ValueError("Validation data is required.")
        truth=[]; pred=[]
        for row in labelled_scores:
            score=row.get("score"); actual=row.get("actual_positive")
            if isinstance(score,bool) or not isinstance(score,(int,float)) or not 0<=score<=100 or actual not in (0,1):
                raise ValueError("Each row needs score 0-100 and actual_positive 0 or 1.")
            truth.append(actual); pred.append(int(score>=threshold))
        return {"threshold":float(threshold),"metrics":self.confusion_metrics(truth,pred),
                "validation_only":True,"production_threshold_changed":False,
                "note":"Requires representative labelled validation data; no real-world accuracy claim is made."}
    @staticmethod
    def score_consistency(round_scores):
        if not isinstance(round_scores,dict): raise TypeError("round_scores must be a dictionary.")
        values=list(round_scores.values())
        if any(isinstance(x,bool) or not isinstance(x,(int,float)) or not 0<=x<=100 for x in values):
            raise ValueError("Round scores must be 0-100.")
        if not values: return {"round_count":0,"mean":None,"range":None,"standard_deviation":None}
        mean=sum(values)/len(values); variance=sum((x-mean)**2 for x in values)/len(values)
        return {"round_count":len(values),"mean":round(mean,2),"range":round(max(values)-min(values),2),
                "standard_deviation":round(variance**.5,2),"interpretation":"descriptive only; rounds measure different constructs"}
