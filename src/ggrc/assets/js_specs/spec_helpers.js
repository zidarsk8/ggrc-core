
/*
 * Generally useful helpers
 * Primarily to support Jasmine 1.3 -> Jasmine 2
 */

// polls check function and calls done when truthy
function waitsFor(check, done) {
    if (!check()) {
        setTimeout(function () {
            waitsFor(check, done);
        }, 1);
    }else{
        done();
    }
};
