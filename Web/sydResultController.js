//
// Part of COMP90024 Cluster and Cloud Computing from The University of Melbourne 
//
// Assignment 2 - Team 20
//
// Collective Team Details (Member's Name/Student ID/Location): 
//
//  * Cenxi Si 1052447 China
//  * Yipei Liu 1067990 China
//  * Jingdan Zhang 1054101 China
//  * Chengyan Dai 1054219 Melbourne
//  * Ruimin Sun 1052182 China
//


const nano = require("nano")("http://admin:170645@172.26.131.170:5984")
// change the profile details
const sydResult = async (req, res) => {
    var db = nano.use('twitter_sentiment_syd')
    var total = []
    var count = 0
    try{
        await db.view('sentiment_analysis','count_sentiment',{group: true}).then((body) => {
            body.rows.forEach((result) => {
                count += result.value
                
            });
            body.rows.forEach((result) => {
                result["percentage"] = (result.value/count*100).toFixed(2)
                total.push(result)
            });
        });
        //return res.send(total)
        return res.render('syd_index',{layout:'main',"thisResult":total})
    } catch (err){
        res.status(400)
        console.log(err)
        return res.send("Internal Error")
    }

}

module.exports = {
    sydResult
}
