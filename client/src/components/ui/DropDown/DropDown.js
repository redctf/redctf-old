import Portal from '../Portal';
import React, { Component } from "react";
import PropTypes from 'prop-types';

export default class DropDown extends Component {
	static displayName = 'DropDown';
	static propTypes = {
		children: PropTypes.node,
		selectedListItem: PropTypes.oneOfType([
			PropTypes.func,
			PropTypes.node
		]),
		selectedListItemStyle: PropTypes.oneOfType([
			PropTypes.object,
			PropTypes.array
		]),
		wrapperClassName: PropTypes.string,
		selectBoxClassName: PropTypes.string,
		menuClassName: PropTypes.string,
		dataAuto: PropTypes.string,
		onClick: PropTypes.func,
		disabled: PropTypes.bool,
		position: PropTypes.string,
		openAbove: PropTypes.bool,
		width: PropTypes.oneOfType([
			PropTypes.string,
			PropTypes.number
		]),
		selectedItem: PropTypes.any
	};

	static defaultProps = {
		selectedItem: 0,
		position: 'right',
		onClick() {}
	};

	constructor(props) {
		super(props);
		this.state = {
			open: false,
			left: 0,
			right: 0,
			bottom: 0,
			menuWidth: 0,
			menuHeight: 0
		};

		this.handleHide = this.handleHide.bind(this);
	}
	componentDidUpdate() {
		if (this.refs.dropDownMenu) {
			if (this.props.openAbove) {
				const menuDimensions = this.refs.dropDownMenu.getBoundingClientRect();
				if (menuDimensions.width !== this.state.menuWidth || menuDimensions.height !== this.state.menuHeight) {
					// Have to get the menu dimensions when it's opened, there is a quick check to see if we already have them (or even need them) before saving them to state to avoid any weird forever rendering states.
					// This is only needed when we need the dropdowns to open upwards instead.. this is really only necessary if the dropdown is at the bottom of the page to avoid weird usability issues.
					this.setState({menuWidth: menuDimensions.width, menuHeight: menuDimensions.height}); // eslint-disable-line react/no-did-update-set-state
				}
			}
			this.refs.dropDownMenu.focus();
		}
	}
	render() {
		// Set the width of the dropdown menu
		// 32 is a magic number this should be fixed to somehow account for the caret itself.
		let dropDownWidth = this.props.width || 'auto';
		let selectedItemWidth = 'calc( 100% - 20px)';

		if (this.props.width) {
			if (!isNaN(parseFloat(dropDownWidth)) && isFinite(dropDownWidth)) {
				selectedItemWidth = (dropDownWidth - 20) + 'px';
				dropDownWidth += 'px';
			} else if (dropDownWidth.indexOf('%') !== -1) {
				selectedItemWidth = `calc( 100% - 20px)`;
			} else {
				selectedItemWidth = (parseInt(dropDownWidth, 10) - 20) + 'px';
			}
		}

		let children = this.props.children;

		// Wrap a selected list item with a component, for example a selected item in the dropdown has a check mark
		if (this.props.selectedListItem) {
			children = React.Children.map(this.props.children, (child, index) => {
				if (index === this.props.selectedItem) {
					let $selectedListItem = this.props.selectedListItem;

					if (typeof $selectedListItem === 'function') {
						$selectedListItem = $selectedListItem();
					}

					// Apply any overriding the normal list item styles
					let styledChild = child;

					if (this.props.selectedListItemStyle) {
						styledChild = React.cloneElement(child, {style: (this.props.selectedListItemStyle)});
					}

					return React.cloneElement($selectedListItem, {children: styledChild});
				}
				return React.cloneElement(child);
			});
		}

		// Set the position for the dropdown menu
		const scrollYPos = window.pageYOffset;
		let menuLeft = this.state.left + 'px';
		let menuTop = this.state.bottom + scrollYPos + 'px';

		if (this.props.openAbove) {
			menuTop = `${this.state.top - this.state.menuHeight}px`;
		}

		if (this.props.position.toLowerCase() === 'left') {
			menuLeft = this.state.right - parseInt(dropDownWidth, 10) + 'px';
		}

		const menuPositionStyle = {
			top: menuTop,
			left: menuLeft,
			width: dropDownWidth
		};

		const dropDownMenu = (
			<Portal isOpened>
				<div data-auto={this.props.dataAuto + '-items'}
					ref='dropDownMenu'
					tabIndex={1}
					onBlur={::this.handleHide}
					onClick={::this.handleToggle}
					className={`drop-down__menu ${this.props.menuClassName}`}
					style={menuPositionStyle}>
					{children}
				</div>
			</Portal>);

		console.log('this.props.children', this.props.children);
		console.log('this.props.selectedItem', this.props.selectedItem);

		// The current item in displayed in the dropbox
		const selectedItem = React.cloneElement(
													this.props.children[this.props.selectedItem],
													{isSelected: true, width: selectedItemWidth});
		return (
			<div ref='dropdown'
				tabIndex='0'
				className={`drop-down__container ${(this.props.disabled && 'drop-down--disabled-cursor') || ''} ${this.props.wrapperClassName}`}
				style={{width: dropDownWidth}}
				onClick={::this.handleToggle}>
				<div className={`drop-down__select-box ${(this.props.disabled && 'drop-down--disabled') || ''} ${this.props.selectBoxClassName}`}
					data-auto={this.props.dataAuto}>
					{selectedItem} <i className={`drop-down__caret ${(this.props.disabled && 'drop-down--disabled') || ''} fa fa-caret-down`}
						ref='indicator'/>
				</div>
				{(this.state.open) ? dropDownMenu : null}
			</div>
		);
	}
	handleToggle(evt) {
		evt.stopPropagation();

		const {left, bottom, top} = this.refs.dropdown.getBoundingClientRect();
		const {right} = this.refs.indicator.getBoundingClientRect();

		this.setState({open: !this.state.open, left, bottom, right, top});
	}
	handleHide() {
		setTimeout(() => {
			if (this.state.open) {
				this.setState({open: false});
			}
		}, 105);
	}
}
