// change the profile details
const analysis = async (req, res) => {
   
    try{
        console.log('11')
        return res.render('analysis',{layout:'main'})
    } catch (err){
        res.status(400)
        console.log(err)
        return res.send("Internal Error")
    }

}

module.exports = {
    analysis
}