import React, { Component } from "react";
import { observer } from "mobx-react";

import Icon from './SvgIcon/Icon';

const Button = ({ ...props }) => {

	return (
		<a className={`custom-button button ${props.class}`}
			onClick={props.onClick}>
			{props.icon && <Icon className='button-icon' type={props.icon} viewBox={props.viewBox}/> }
			{props.title}
		</a>
	)
};

export default Button;
