// event details

let event_details_options = document.querySelectorAll('.event_details__bottom__overview__left_right__options__select span')
let event_details_options_boxes = document.querySelectorAll('.event_details__bottom__overview__left_right__options__bottom')

event_details_options.forEach(option => {
	option.addEventListener('click', function(){
		event_details_options.forEach(option => {
			option.style.color = 'black';
		})
		event_details_options_boxes.forEach(box => {
			box.classList.remove('event_details-active')
		})
		let optionCode = option.dataset.eventdetailsoption
		document.querySelector(`.event_details__bottom__overview__left_right__options__bottom[data-eventDetailsOption="${optionCode}"]`).classList.add('event_details-active')
		option.style.color = 'red';
	})
})