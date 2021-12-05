$(document).ready(function () {
    // example: https://getbootstrap.com/docs/4.2/components/modal/
    // show modal
    $('#sp-modal').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget)
        const LPId = button.data('source') 
        const modal = $(this)
        modal.find('.modal-title').text("Run Procedure")
        // $('#task-form-display').removeAttr('LPId')
    })
    $('#submit-sp').click(function () {
        // const tID = $('#task-form-display').attr('LPId');
        // console.log($('#task-modal').find('.form-control').val()[1])
        $.ajax({
            type: 'GET',
            url: '/procedure/',
            //contentType: 'application/json;charset=UTF-8',
            data: {"leaseOption": $('#sp-modal').find('.sp-input').val()},
            success: function (res) {
                console.log(res.response)
                location.assign(this.url);
            },
            error: function () {
                console.log('Error');
            }
        });
    });
    $('#task-modal').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget) // Button that triggered the modal
        const LPId = button.data('source') // Extract info from data-* attributes
        const LPName = button.data('name') // Extract info from data-* attributes
        const address = button.data('address')
        const price = button.data('price')
        const rating = button.data('rating')
        const leaseOption = button.data('leaseoption')
        const website = button.data('website')
        const modal = $(this)
        // console.log(LPId,LPName,address,price,rating)
        if (LPId === 'New LivePlace') {
            modal.find('.modal-title').text(LPId)
            $('#task-form-display').removeAttr('LPId')
        } else {
            modal.find('.modal-title').text('Edit LivePlace ' + LPId)
            $('#task-form-display').attr('LPId', LPId)
        }

        if (LPName) {
            modal.find('.name-input').val(LPName);
        } else {
            modal.find('.name-input').val('');
        }

        if (address) {
            modal.find('.address-input').val(address);
        } else {
            modal.find('.address-input').val('');
        }

        if (price) {
            modal.find('.price-input').val(price);
        } else {
            modal.find('.price-input').val('');
        }

        if (rating) {
            modal.find('.rating-input').val(rating);
        } else {
            modal.find('.rating-input').val('');
        }

        if (leaseOption) {
            modal.find('.leaseOption-input').val(leaseOption);
        } else {
            modal.find('.leaseOption-input').val('');
        }

        if (website) {
            modal.find('.website-input').val(website);
        } else {
            modal.find('.website-input').val('');
        }

    })


    $('#submit-LivePlace').click(function () {
        const tID = $('#task-form-display').attr('LPId');
        console.log($('#task-modal').find('.form-control').val()[1])
        $.ajax({
            type: 'POST',
            url: tID ? '/edit/' + tID : '/create',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'LPName': $('#task-modal').find('.name-input').val(),
                'address': $('#task-modal').find('.address-input').val(),
                'price': $('#task-modal').find('.price-input').val(),
                'rating': $('#task-modal').find('.rating-input').val(),
                'leaseOption': $('#task-modal').find('.leaseOption-input').val(),
                'website': $('#task-modal').find('.website-input').val()
            }),
            success: function (res) {
                console.log(res.response)
                if (res.success==false){
                    alert("Something went wrong");
                }
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('.remove').click(function () {
        const remove = $(this)
        $.ajax({
            type: 'POST',
            url: '/delete/' + remove.data('source'),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });




    // $('.state').click(function () {
    //     const state = $(this)
    //     const tID = state.data('source')
    //     const new_state
    //     if (state.text() === "In Progress") {
    //         new_state = "Complete"
    //     } else if (state.text() === "Complete") {
    //         new_state = "Todo"
    //     } else if (state.text() === "Todo") {
    //         new_state = "In Progress"
    //     }

    //     $.ajax({
    //         type: 'POST',
    //         url: '/edit/' + tID,
    //         contentType: 'application/json;charset=UTF-8',
    //         data: JSON.stringify({
    //             'status': new_state
    //         }),
    //         success: function (res) {
    //             console.log(res)
    //             location.reload();
    //         },
    //         error: function () {
    //             console.log('Error');
    //         }
    //     });
    // });

});